import uuid
from datetime import datetime
import os
import json
import streamlit as st
import ollama

# ---------- PATHS & CONFIG ----------
HISTORY_FILE = os.path.join(os.path.dirname(__file__), "history.json")
MODEL_NAME = "llama3"

# ---------- HISTORY HELPERS ----------
def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []
    return []

def save_history(history):
    tmp_path = HISTORY_FILE + ".tmp"
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=4, ensure_ascii=False)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp_path, HISTORY_FILE)

def make_conversation(messages, title=None, conv_id=None):
    if conv_id is None:
        conv_id = str(uuid.uuid4())

    if not title:
        first_user = next((m["content"] for m in messages if m.get("role") == "user"), None)
        title = (first_user[:60] + "...") if first_user else f"Conversation {datetime.utcnow().isoformat()}"

    return {
        "id": conv_id,
        "title": title,
        "messages": messages,
        "created_at": datetime.utcnow().isoformat()
    }

def fmt_time(iso_ts):
    try:
        return datetime.fromisoformat(iso_ts).strftime("%Y-%m-%d %H:%M")
    except Exception:
        return iso_ts or "-"

def safe_rerun():
    rerun = getattr(st, "experimental_rerun", None)
    if callable(rerun):
        rerun()
    else:
        st.session_state["_rerun_flag"] = not st.session_state.get("_rerun_flag", False)

# ---------- INITIALIZATION ----------
if "initialized" not in st.session_state:
    st.session_state.conversations = load_history()
    st.session_state.messages = []
    st.session_state.context_messages = []
    st.session_state.current_conversation_id = None
    st.session_state["_rerun_flag"] = False
    st.session_state.initialized = True
    st.session_state.selected_conv = "New Chat"
    st.session_state.last_selected = "New Chat"

# ---------- SIDEBAR ----------
st.sidebar.title("History")

# Create new conversation
if st.sidebar.button("New Chat"):
    if st.session_state.messages:
        new_conv = make_conversation(st.session_state.messages.copy())
        st.session_state.conversations.insert(0, new_conv)
        save_history(st.session_state.conversations)

    st.session_state.messages = []
    st.session_state.context_messages = []
    st.session_state.current_conversation_id = None
    st.session_state.selected_conv = "New Chat"
    st.session_state.last_selected = "New Chat"
    safe_rerun()

# Build dropdown labels
conv_labels = ["New Chat"] + [
    f"{i+1}: {c['title']} ({fmt_time(c.get('created_at'))})"
    for i, c in enumerate(st.session_state.conversations)
]

# Ensure valid state
if st.session_state.selected_conv not in conv_labels:
    st.session_state.selected_conv = "New Chat"
    st.session_state.last_selected = "New Chat"

# Selection Dropdown
selected = st.sidebar.selectbox(
    "Select conversation",
    conv_labels,
    index=conv_labels.index(st.session_state.selected_conv),
    key="selected_conv"
)

# If selection changed, load conversation
if st.session_state.selected_conv != st.session_state.last_selected:
    sel = st.session_state.selected_conv
    st.session_state.last_selected = sel

    if sel != "New Chat":
        idx = int(sel.split(":")[0]) - 1
        conv = st.session_state.conversations[idx]
        st.session_state.messages = conv["messages"].copy()
        st.session_state.current_conversation_id = conv["id"]
    else:
        st.session_state.messages = []
        st.session_state.context_messages = []
        st.session_state.current_conversation_id = None

    safe_rerun()

# Show details for selected conversation
if st.session_state.last_selected != "New Chat":
    idx = int(st.session_state.last_selected.split(":")[0]) - 1
    conv = st.session_state.conversations[idx]
    st.sidebar.write(f"Created: {fmt_time(conv.get('created_at'))}")

    if st.sidebar.button("Use as Context"):
        st.session_state.context_messages = conv["messages"].copy()
        st.session_state.current_conversation_id = None
        st.sidebar.success("Context loaded!")

    if st.sidebar.button("Delete Conversation"):
        removed = st.session_state.conversations.pop(idx)
        save_history(st.session_state.conversations)

        if st.session_state.current_conversation_id == removed["id"]:
            st.session_state.messages = []
            st.session_state.current_conversation_id = None

        st.session_state.selected_conv = "New Chat"
        st.session_state.last_selected = "New Chat"
        safe_rerun()

# Show all history (optional)
if st.sidebar.checkbox("Show all history"):
    for i, c in enumerate(st.session_state.conversations):
        st.sidebar.markdown(f"- **{i+1}. {c['title']}** ({fmt_time(c['created_at'])})")

# ---------- MAIN CHAT UI ----------
st.title("💬 Local AI Chatbot (Ollama)")

# Show context
if st.session_state.context_messages:
    with st.expander("Context messages (hidden from model view)"):
        for m in st.session_state.context_messages:
            role = m["role"]
            st.write(f"**{role}**: {m['content']}")

# Show previous messages
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# ---------- USER INPUT ----------
user_input = st.chat_input("Type your message")

if user_input:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    # Build payload for Ollama
    combined_messages = st.session_state.context_messages + st.session_state.messages

    try:
        response = ollama.chat(model=MODEL_NAME, messages=combined_messages)
        reply = response.get("message", {}).get("content", "")
    except Exception as e:
        reply = f"Error: {e}"

    # Add bot message
    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.chat_message("assistant").write(reply)

    # Update history if editing an existing one
    if st.session_state.current_conversation_id:
        for c in st.session_state.conversations:
            if c["id"] == st.session_state.current_conversation_id:
                c["messages"] = st.session_state.messages.copy()
                save_history(st.session_state.conversations)
                break


import ollama

def chat_with_model(model_name="llama3"):
    print(f"🚀 Chatbot is running using model: {model_name}")
    print("Type 'exit' to stop\n")

    chat_history = []

    while True:
        user_input = input("You: ")

        if user_input.lower() == "exit":
            print("Chat ended.")
            break

        chat_history.append({"role": "user", "content": user_input})

        response = ollama.chat(model=model_name, messages=chat_history)

        reply = response['message']['content']
        print(f"{model_name}: {reply}\n")

        chat_history.append({"role": "assistant", "content": reply})


if __name__ == "__main__":
    chat_with_model()

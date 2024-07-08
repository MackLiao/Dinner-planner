import openai
import os

# Set the API key and organization
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.organization = os.getenv("OPENAI_ORGANIZATION")

# Function to chat with the OpenAI model
def chat_with_openai():
    messages = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Ending chat.")
            break

        messages.append({"role": "user", "content": user_input})

        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=messages
        )

        assistant_response = response.choices[0].message['content']
        print(f"Assistant: {assistant_response}")

        messages.append({"role": "assistant", "content": assistant_response})

if __name__ == "__main__":
    chat_with_openai()
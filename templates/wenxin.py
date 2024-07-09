import requests
import json

API_KEY = "aia2zXeMrnZMqqBBmEyqUeVJ"
SECRET_KEY = "AMk6O7N08K8EHzJ9U4sqpyqOuF7l2FoN"

def get_access_token():
    """
    Use AK and SK to generate an authentication signature (Access Token)
    :return: access_token, or None (if error)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {
        "grant_type": "client_credentials",
        "client_id": API_KEY,
        "client_secret": SECRET_KEY
    }
    response = requests.post(url, params=params).json()
    return response.get("access_token")

def chat_with_bot():
    """
    Main function to interact with the Baidu AI chatbot.
    """
    access_token = get_access_token()
    if not access_token:
        print("Failed to obtain access token")
        return

    url = f"https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/eb-instant?access_token={access_token}"
    headers = {
        'Content-Type': 'application/json'
    }

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Exiting the chat.")
            break

        payload = json.dumps({
            "messages": [
                {
                    "role": "user",
                    "content": user_input
                }
            ]
        })

        response = requests.post(url, headers=headers, data=payload).json()
        print(f"Bot: {response.get('result')}")

if __name__ == '__main__':
    chat_with_bot()

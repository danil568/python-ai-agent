import requests

API_KEY = "your_openrouter_api_key_here"

SYSTEM_PROMPT = "Ты саркастичный помощник который отвечает с юмором но всегда даёт правильный совет в конце. Обращайся к пользователю на ты."

conversation = [
    {"role": "system", "content": SYSTEM_PROMPT}
]

headers = {
    "Authorization": "Bearer " + API_KEY,
    "Content-Type": "application/json"
}

print("AI chat started! Type 'exit' to stop.")
print("-" * 40)

while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break

    conversation.append({"role": "user", "content": user_input})

    data = {
        "model": "openrouter/free",
        "messages": conversation
    }

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json=data
    )

    result = response.json()
    if "choices" in result:
        ai_reply = result["choices"][0]["message"].get("content") or result["choices"][0]["message"].get("reasoning") or "нет ответа"
        conversation.append({"role": "assistant", "content": ai_reply})
        print("AI: " + str(ai_reply or "..."))
    else:
        print("Error: " + str(result.get("error", {}).get("message", "Unknown")))
    print()
import requests
import json
from datetime import datetime

API_KEY = "your_openrouter_api_key_here"
WEATHER_KEY = "2b8dd1a72a41d24e913fa0eac6d7a854"

def get_current_time():
    return datetime.now().strftime("%H:%M:%S")

def calculate(expression):
    try:
        return str(eval(expression))
    except:
        return "Ошибка в выражении"

def get_weather(city):
    url = f"https://wttr.in/{city}?format=3&lang=ru"
    r = requests.get(url, timeout=10)
    return r.text
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "Возвращает текущее время",
            "parameters": {"type": "object", "properties": {}}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Вычисляет математическое выражение",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {"type": "string", "description": "Математическое выражение например 2+2"}
                },
                "required": ["expression"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Возвращает текущую погоду в городе",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "Название города на английском"}
                },
                "required": ["city"]
            }
        }
    }
]

headers = {
    "Authorization": "Bearer " + API_KEY,
    "Content-Type": "application/json"
}

print("Агент с инструментами запущен! Введите 'exit' для выхода.")
print("-" * 40)

while True:
    user_input = input("Вы: ")
    if user_input.lower() == "exit":
        break

    messages = [{"role": "user", "content": user_input}]

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json={"model": "openrouter/free", "messages": messages, "tools": TOOLS}
    )

    result = response.json()
    message = result["choices"][0]["message"]

    if message.get("tool_calls"):
        tool_call = message["tool_calls"][0]
        tool_name = tool_call["function"]["name"]
        tool_args = json.loads(tool_call["function"]["arguments"] or "{}")

        print(f"🔧 Агент вызвал инструмент: {tool_name}")

        if tool_name == "get_current_time":
            tool_result = get_current_time()
        elif tool_name == "calculate":
            tool_result = calculate(tool_args.get("expression", ""))
        elif tool_name == "get_weather":
            tool_result = get_weather(tool_args.get("city", ""))

        print(f"📊 Результат: {tool_result}")

        messages.append(message)
        messages.append({"role": "tool", "tool_call_id": tool_call["id"], "content": tool_result})

        final = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json={"model": "openrouter/free", "messages": messages}
        )
        reply = final.json()["choices"][0]["message"].get("content", "")
        print(f"AI: {reply}")
    else:
        print(f"AI: {message.get('content', '')}")
    print()
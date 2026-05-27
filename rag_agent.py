import requests

API_KEY = "your_openrouter_api_key_here"
def load_knowledge(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return f.read()

def ask_with_context(question, knowledge):
    headers = {
        "Authorization": "Bearer " + API_KEY,
        "Content-Type": "application/json"
    }

    messages = [
        {
            "role": "system",
            "content": "Ты помощник компании по натяжным потолкам. Отвечай ТОЛЬКО на основе информации ниже. Если информации нет — скажи что не знаешь.\n\nБАЗА ЗНАНИЙ:\n" + knowledge
        },
        {
            "role": "user",
            "content": question
        }
    ]

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json={"model": "openrouter/free", "messages": messages}
    )

    result = response.json()
    if "choices" in result:
        return result["choices"][0]["message"].get("content", "Нет ответа")
    else:
        return f"Ошибка: {result.get('error', {}).get('message', str(result))}"

knowledge = load_knowledge("knowledge.txt")
print("База знаний загружена!")
print("Задавай вопросы. Введи 'exit' для выхода.")
print("-" * 40)

while True:
    question = input("Вы: ")
    if question.lower() == "exit":
        break
    answer = ask_with_context(question, knowledge)
    print(f"Бот: {answer}")
    print()
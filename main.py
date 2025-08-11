import json
import os

from langchain_gigachat.chat_models import GigaChat
from langchain.schema import SystemMessage, HumanMessage
from sys_prompts import sys_prompts
from test_data import clients, dialogs
from dotenv import load_dotenv
load_dotenv()
giga_auth = os.getenv("GIGACHAT_AUTH")


# ВЫБОР ЦЕПОЧКИ (1-4)
print(f"""Выберите номер цепочки промптов
        1 - Нужна Детская карта, не нужен Сбер Мобайл
        2 - Не нужна Детская карта, нужен Сбер Мобайл
        3 - Обе услуги востребованы
        4 - Ничего не надо
Введите номер: """
      )
i = int(input())



giga = GigaChat(
    model = 'gigachat-2-max',
    credentials=giga_auth,
    scope = "GIGACHAT_API_PERS",
    verify_ssl_certs=False,
    temperature=0,
    top_p=0.1,
    timeout=60.0
)

print(f"\n\nЭтап 1: packege_sale")

response = giga.invoke([
        SystemMessage(content=sys_prompts[0]),
        HumanMessage(content=f"{clients[i - 1]}\n\ndialogue:\n{dialogs[i - 1]}")
    ])
response_content = response.content.strip('```')
print(response_content)

response_json = json.loads(response_content)




print(f"\n\nЭтап 2: ai-sale-speaker")

response = giga.invoke([
        SystemMessage(content=sys_prompts[1]),
        HumanMessage(content=f"client:\n{clients[i - 1]}\n\ndialogue:\n{dialogs[i - 1]}")
    ])

response_content = response.content.strip('```')
print(response_content)





print(f"\n\nЭтап 3: ai-speaker-package")

response = giga.invoke([
        SystemMessage(content=sys_prompts[2]),
        HumanMessage(content=f"client:\n{clients[i - 1]}\n\ndialogue:\n{dialogs[i - 1]}")
    ])
print(response.content)
print("\nГотово!")

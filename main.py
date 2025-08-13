import json
import os
from gigachat import GigaChat
from gigachat.models import Chat, Messages, MessagesRole
from sys_prompts import sys_prompts
from test_data import clients, dialogs
from dotenv import load_dotenv

load_dotenv()
giga_auth = os.getenv("GIGACHAT_AUTH")
from products_list import products

total_prompt_tokens = 0
total_completion_tokens = 0
total_tokens = 0

# ВЫБОР ЦЕПОЧКИ (1-4)
print(f"""Выберите номер первой цепочки промптов
        1 - Нужна Детская карта, не нужен Сбер Мобайл
        2 - Не нужна Детская карта, нужен Сбер Мобайл
        3 - Обе услуги востребованы
        4 - Ничего не надо
Введите номер: """
	  )
i = int(input())

print(f"""Выберите второй цепочки промптов
        0 - Не нужно прилагать каталог продуктов
        1 - Только СберМобайл и Детская карта
        2 - Прилагается весь каталог продуктов
Введите номер: """)
j = int(input())
if j == 2:
	products_num = f"{products[0]}\n\n{products[1]}"
else:
	products_num = products[j]

giga = GigaChat(
	credentials=giga_auth,
	scope="GIGACHAT_API_PERS",
	verify_ssl_certs=False
)

print(f"\n\nЭтап 1: packege_sale")
messages = [
	Messages(role=MessagesRole.SYSTEM, content=sys_prompts[0]),
	# \n\ndialogue:\n{dialogs[i - 1]}
	Messages(role=MessagesRole.USER, content=f"{clients[i - 1]}\n\nproducts:\n{products_num}")
]
payload = Chat(
	messages=messages,
	model='GigaChat-2-max',
	temperature=0,
	top_p=0.1
)
response = giga.chat(payload)
response_content = response.choices[0].message.content.strip('```')
print(response_content)

stage1_prompt_tokens = response.usage.prompt_tokens
stage1_completion_tokens = response.usage.completion_tokens
stage1_total_tokens = response.usage.total_tokens
total_prompt_tokens += stage1_prompt_tokens
total_completion_tokens += stage1_completion_tokens
total_tokens += stage1_total_tokens
print(f"\nТокены на этапе 1:")
print(f"  Токены на запрос (prompt_tokens): {stage1_prompt_tokens}")
print(f"  Токены на ответ (completion_tokens): {stage1_completion_tokens}")
print(f"  Общее количество токенов (total_tokens): {stage1_total_tokens}")

response_json = json.loads(response_content)

print(f"\n\nЭтап 2: ai-sale-speaker")
messages = [
	Messages(role=MessagesRole.SYSTEM, content=sys_prompts[1]),
	# \n\ndialogue:\n{dialogs[i - 1]}
	Messages(role=MessagesRole.USER, content=f"client:\n{clients[i - 1]}")
]
payload = Chat(
	messages=messages,
	model='GigaChat-2-max',
	temperature=0,
	top_p=0.1
)
response = giga.chat(payload)
response_content = response.choices[0].message.content.strip('```')
print(response_content)

stage2_prompt_tokens = response.usage.prompt_tokens
stage2_completion_tokens = response.usage.completion_tokens
stage2_total_tokens = response.usage.total_tokens
total_prompt_tokens += stage2_prompt_tokens
total_completion_tokens += stage2_completion_tokens
total_tokens += stage2_total_tokens
print(f"\nТокены на этапе 2:")
print(f"  Токены на запрос (prompt_tokens): {stage2_prompt_tokens}")
print(f"  Токены на ответ (completion_tokens): {stage2_completion_tokens}")
print(f"  Общее количество токенов (total_tokens): {stage2_total_tokens}")

print(f"\n\nЭтап 3: ai-speaker-package")
messages = [
	Messages(role=MessagesRole.SYSTEM, content=sys_prompts[2]),
	# \n\ndialogue:\n{dialogs[i - 1]}
	Messages(role=MessagesRole.USER, content=f"client:\n{clients[i - 1]}")
]
payload = Chat(
	messages=messages,
	model='GigaChat-2-max',
	temperature=0,
	top_p=0.1
)
response = giga.chat(payload)
response_content = response.choices[0].message.content
print(response_content)

stage3_prompt_tokens = response.usage.prompt_tokens
stage3_completion_tokens = response.usage.completion_tokens
stage3_total_tokens = response.usage.total_tokens
total_prompt_tokens += stage3_prompt_tokens
total_completion_tokens += stage3_completion_tokens
total_tokens += stage3_total_tokens
print(f"\nТокены на этапе 3:")
print(f"  Токены на запрос (prompt_tokens): {stage3_prompt_tokens}")
print(f"  Токены на ответ (completion_tokens): {stage3_completion_tokens}")
print(f"  Общее количество токенов (total_tokens): {stage3_total_tokens}")

print("\nГотово!")

print(f"\nОбщая статистика использования токенов:")
print(f"  Токены на запросы (prompt_tokens): {total_prompt_tokens}")
print(f"  Токены на ответы (completion_tokens): {total_completion_tokens}")
print(f"  Общее количество токенов (total_tokens): {total_tokens}")

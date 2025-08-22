import os
from gigachat import GigaChat
from gigachat.models import Chat, Messages, MessagesRole

from new_prompt import sys_prompt, advantages, clients, politeness
from dotenv import load_dotenv

load_dotenv()
giga_auth = os.getenv("GIGACHAT_AUTH")

total_prompt_tokens = 0
total_completion_tokens = 0
total_tokens = 0

print(f"""Выберите продукт
        1 - СберЗдоровье
        2 - ПДС
        3 - ЗЛС
        4 - СберПрайм (ДОПИСАТЬ)
        5 - Кредитная карта
Введите номер: """)
j = int(input())

print(f"""Выберите номер клиентов
        1 - Клиент 1 (айтишник)
        2 - Клиент 2 (бабка)
        3 - Клиент 3 (студентик)
        4 - Клиент 4 (темщик)
        5 - Клиент 5 (VIP клиентик)
Введите номер: """)
i = int(input())

giga = GigaChat(
	credentials=giga_auth,
	scope="GIGACHAT_API_B2B",
	verify_ssl_certs=False
)

print(f"\n\nЭтап 1: packege_sale")
messages = [
	Messages(role=MessagesRole.SYSTEM, content=f"{sys_prompt}\n\nИспользуй такой стиль общения:\n{politeness}"),
	# \n\ndialogue:\n{dialogs[i - 1]}
	Messages(role=MessagesRole.USER, content=f"{advantages[j - 1]}\n\n{clients[i - 1]}")
]

payload = Chat(
	messages=messages,
	model='GigaChat-2-Max',
	temperature=0,
	top_p=0.1
)
response = giga.chat(payload)
response_content_1 = response.choices[0].message.content.strip('```')
print(response_content_1)

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

'''print(f"\n\nЭтап 2: ai-sale-speaker")
messages = [
	Messages(role=MessagesRole.SYSTEM, content=sys_prompts[1]),
	# \n\ndialogue:\n{dialogs[i - 1]}
	Messages(role=MessagesRole.USER, content=f"client:\n{clients[i-1]}")
]
payload = Chat(
	messages=messages,
	model='GigaChat-2-max',
	temperature=0,
	top_p=0.1
)
response = giga.chat(payload)
response_content_2 = response.choices[0].message.content.strip('```')
print(response_content_2)

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
	Messages(role=MessagesRole.USER, content=f"client:\n{clients[i-1]}\n\nproducts:\n{products}\n\npackage_products:\n{response_content_1}")
]
payload = Chat(
	messages=messages,
	model='GigaChat-2-max',
	temperature=0,
	top_p=0.1
)
response = giga.chat(payload)
response_content_3 = response.choices[0].message.content
print(response_content_3)

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
'''

print("\nГотово!")

print(f"\nОбщая статистика использования токенов:")
print(f"  Токены на запросы (prompt_tokens): {total_prompt_tokens}")
print(f"  Токены на ответы (completion_tokens): {total_completion_tokens}")
print(f"  Общее количество токенов (total_tokens): {total_tokens}")

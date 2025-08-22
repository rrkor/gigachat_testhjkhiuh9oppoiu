import os

from dotenv import load_dotenv
from gigachat import GigaChat
from gigachat.models import Messages, MessagesRole, Chat

# from products import products
from random import randint

from synergy import synergy

load_dotenv()
giga_auth = os.getenv("GIGACHAT_AUTH")

sys_prompt_summary = """
Ты получаешь на вход информацию о трёх продуктах. Для каждого продукта будут даны:

Название
Ключевые преимущества для пользователя (личная ценность/выгоды)
Возможные связи или дополнения с другими продуктами
Задача:
Проанализируй три продукта.
Определи, как их можно связать между собой в единую логическую систему или пакетное предложение.
Построй связку так, чтобы каждый продукт усиливал ценность других.
В ответ верни средней длинны абзац, в котором будешь рассказывать клиенту о том, 
почему для него выгодно использование данных товаров, не сильно повторяйся с информацией, которая была предоставлена тебе.

Требования по стилю написания:
Понятным разговорным языком! Без разметки MarkDown! До 70 слов! Пиши конкретнее, используй числа и пиши конкретную выгоду
Не пиши ничего про общую выгоду и экономию, описывай выгоду только по продуктам отдельно.

Вот тебе пример ОТЛИЧНОГО ответа:
"Предлагаемый пакет продуктов позволит Вам существенно сэкономить и повысить комфорт взаимодействия с нашим банком. 
СберПрайм упростит ваши службы и откроет доступ к дополнительным выгодным сервисам. 
Накопительный счёт обеспечит постоянный доход от ваших свободных средств. 
Кредитная карта упростит управление финансами и позволит быстрее распоряжаться деньгами, сохранив капитал на вкладе."

Сохрани стиль и структуру из данного примера
"""
import json
with open("output.json", "r", encoding='utf-8') as file:
	products = json.load(file)


prod = []
relevant_products = []
for i in range(0, 3):
	prod.append(randint(0, 8))
print(prod)

for j in prod:
	relevant_products.append(products[j] + synergy[j])
	print(f"{products[j]}")

giga = GigaChat(
	credentials=giga_auth,
	scope="GIGACHAT_API_B2B",
	verify_ssl_certs=False
)

messages = [
	Messages(role=MessagesRole.SYSTEM, content=f"{sys_prompt_summary}"),
	Messages(role=MessagesRole.USER,
			 content=f"Вот список продуктов и их связки с другими продуктами:\n\n{relevant_products}")
]

payload = Chat(
	messages=messages,
	model='GigaChat-2-Max',
	temperature=0,
	top_p=0.1,
	profanity_check=False,
)

response = giga.chat(payload)
print(response.choices[0].message.content)

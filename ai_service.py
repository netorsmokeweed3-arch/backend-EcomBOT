import os
import anthropic

# Зчитуємо API-ключ зі змінних оточення сервера
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

def process_order_and_chat_with_ai(order_data, chat_messages):
    prompt = f"""
    Ти — розумний AI-помічник для продавця на маркетплейсі Prom.ua. 
    Проаналізуй замовлення та історію чату з покупцем.
    
    Дані замовлення:
    {order_data}
    
    Історія чату / повідомлень:
    {chat_messages}
    
    Зроби наступне:
    1. Структуруй інформацію про клієнта та товари (ПІБ, телефон, адреса, статус).
    2. Проаналізуй, чи є товари в наявності, і сформуй звіт.
    3. Сформуй короткий і ввічливий варіант відповіді для покупця (якщо потрібна відповідь на його запитання в чаті).
    4. Зроби висновок: замовлення підтверджено, очікує чи є відмова.
    """

    try:
        response = client.messages.create(
            model="claude-haiku-5-5",
            max_tokens=1000,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response.content[0].text
    except Exception as e:
        print("Помилка при зверненні до Claude API:", e)
        return f"Помилка обробки даних через штучний інтелект: {str(e)}"
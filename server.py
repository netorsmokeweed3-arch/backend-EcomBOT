import os
from flask import Flask, jsonify, request
import requests
from ai_service import process_order_and_chat_with_ai

app = Flask(__name__)

# Твій токен доступу до Prom.ua API
PROM_TOKEN = "3f7ee5349834e4721e43904eb1119c94db65a83c"
PROM_API_URL = "https://my.prom.ua/api/v1/orders/list"

@app.route("/")
def home():
    return "EcomBot Backend with AI is running successfully! 🚀"

# Маршрут для отримання замовлень з Prom.ua
@app.route("/api/orders", methods=["GET"])
def get_orders():
    headers = {
        "Authorization": f"Bearer {PROM_TOKEN}",
        "Content-Type": "application/json",
    }

    try:
        response = requests.get(PROM_API_URL, headers=headers)

        if response.status_code == 200:
            data = response.json()
            orders = data.get("orders", [])
            return jsonify({"success": True, "orders": orders})
        else:
            print(f"Помилка Prom API: {response.status_code}, {response.text}")
            return jsonify({
                "success": False,
                "message": f"Помилка від Prom API: {response.status_code}"
            }, 500)

    except Exception as e:
        print(f"Виняток при запиті до Пром: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

# Маршрут для обробки замовлень та чатів через Claude Haiku через той самий сервер
@app.route("/api/process-ai", methods=["POST"])
def process_ai():
    try:
        req_data = request.json
        order_data = req_data.get("order_data", "")
        chat_messages = req_data.get("chat_messages", "")

        # Викликаємо функцію штучного інтелекту з ai_service.py
        ai_response = process_order_and_chat_with_ai(order_data, chat_messages)

        return jsonify({
            "success": True,
            "ai_report": ai_response
        })
    except Exception as e:
        print(f"Помилка ШІ маршруту: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
from fastapi import FastAPI, Request
import uvicorn
import json

# Создаем экземпляр приложения FastAPI
app = FastAPI(title="Request Logger API")


@app.post("/log-request")
async def log_request(request: Request):
    """
    Эндпоинт для логирования входящих POST-запросов.
    Логирует заголовки, тело запроса и другую информацию.
    """

    # Получаем данные из запроса
    client_host = request.client.host
    method = request.method
    url = str(request.url)
    headers = dict(request.headers)

    # Пытаемся получить тело запроса в разных форматах
    try:
        # Для JSON данных
        body = await request.json()
        body_type = "JSON"
    except:
        try:
            # Для form-data
            body = await request.form()
            body_type = "FORM"
            body = dict(body)
        except:
            # Для plain text или других форматов
            body = await request.body()
            body_type = "RAW"
            try:
                body = body.decode('utf-8')
            except:
                body = str(body)

    # Формируем лог-сообщение
    log_message = f"""
╔═══════════════════════════════════════════════════════════════
║ POST Request Received
╠═══════════════════════════════════════════════════════════════
║ From: {client_host}
║ URL: {url}
║ Method: {method}
║ Body Type: {body_type}
╠═══════════════════════════════════════════════════════════════
║ Headers:
{json.dumps(headers, indent=2, ensure_ascii=False)}
╠═══════════════════════════════════════════════════════════════
║ Body:
{json.dumps(body, indent=2, ensure_ascii=False) if isinstance(body, (dict, list)) else body}
╚═══════════════════════════════════════════════════════════════
"""

    # Выводим в консоль
    print(log_message)

    return {
        "status": "success",
        "message": "Request logged successfully",
        "client_ip": client_host,
        "body_type": body_type,
        "body_received": body
    }


@app.get("/")
async def root():
    """Корневой эндпоинт с инструкциями"""
    return {
        "message": "Request Logger API is running!",
        "usage": "Send POST request to /log-request endpoint",
        "example_curl": "curl -X POST -H 'Content-Type: application/json' -d '{\"test\": \"data\"}' http://localhost:8000/log-request"
    }


if __name__ == "__main__":
    # Запускаем сервер
    print("Starting Request Logger API server...")
    print("Send POST requests to http://localhost:8000/log-request")
    print("Press Ctrl+C to stop the server")

    uvicorn.run(app, host="0.0.0.0", port=8000)



import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
import g4f

app = FastAPI(title="Cyber-Lab Portfolio")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(BASE_DIR, "templates", "index.html")

class UserMessage(BaseModel):
    message: str

@app.get("/")
async def home():
    if not os.path.exists(FILE_PATH):
        raise HTTPException(status_code=404, detail="Файл index.html не найден")
    return FileResponse(FILE_PATH)

@app.post("/api/chat")
async def chat_endpoint(data: UserMessage):
    user_text = data.message.strip()
    
    try:
        # Запрос к живому ИИ (используем модель gpt-4o или аналогичную доступную)
        response = await g4f.ChatCompletion.create_async(
            model=g4f.models.default,
            messages=[
                {"role": "system", "content": "Ты — продвинутый ИИ-ассистент на сайте талантливого Python-разработчика и инженера автоматизации. Отвечай коротко, профессионально, в стиле киберпанк-терминала (используй знаки ►). Помогай продавать услуги создания Telegram-ботов, парсеров и бэкенда."},
                {"role": "user", "content": user_text}
            ]
        )
        reply = f"► ИИ_АНАЛИЗ: {response}"
    except Exception:
        # Резервный вариант, если сеть провайдера занята
        user_lower = user_text.lower()
        if "привет" in user_lower:
            reply = "► СИСТЕМА: Соединение установлено. Рад приветствовать в терминале разработки."
        elif "бот" in user_lower or "telegram" in user_lower:
            reply = "► МОДУЛЬ_ТГ: Создание ботов любой сложности (ИИ, базы данных, вебхуки). Разработка от 3 дней."
        elif "цена" in user_lower or "стоимость" in user_lower:
            reply = "► ЛОГ_ЦЕН: Скрипты от $50, ИИ-системы от $200. Для точной сметы свяжитесь по контактам ниже."
        else:
            reply = f"► ПРИНЯТО: Запрос «{user_text}» зафиксирован. Свяжитесь с разработчиком напрямую в Telegram."

    return {"response": reply}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
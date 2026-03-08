# AI API

FastAPI Backend-проект з запитами за допомогою Claude API для аналізу тексту і обробки запитів, Session-based chat with Async + Redis

**Стек:** Python 3.12 · FastAPI · Claude API · Redis

## Швидкий старт

```bash
git clone <repo>
cd ai_api

docker run -d -p 6379:6379 redis:alpine

uvicorn main:app --reload
```


## Endpoints

| Назва | Метод | Навіщо |
|------|-----|--------|
| `/summarize` | POST | Короткий зміст на основі тексту |
| `/analyze-sentiment` | POST | Аналіз змісту тексту |
| `/ask` |  POST | Відповіді на питання на основі заданого тексту |
| `/chat` | POST | формат `/ask` з історією |
| `/session-chat` | POST | Session-based chat with Redis |


## Особливості
- Аналіз тексту за допомогою AI з збереженням запитів
- Redis для розділення чатів на сесії

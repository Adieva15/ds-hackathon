from ai_coach import get_gigachat_token
import asyncio

async def test():
    print("🔍 Проверяем исправления...")
    token = get_gigachat_token()
    if token:
        print("✅ Всё работает! Токен получен успешно")
        print(f"Токен: {token[:30]}...")
    else:
        print("❌ Есть проблемы с получением токена")

if __name__ == "__main__":
    asyncio.run(test())
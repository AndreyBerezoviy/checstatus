import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import Command
from playwright.async_api import async_playwright
from datetime import datetime

API_TOKEN = 'YOUR_API_TOKEN'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

user_chat_ids = set()

#Ссылки на свервера, которые нужны
url_to_server = {
    'https://portal.cherryservers.com/deployment?plan=804&tags=up_to_16': "AMD Ryzen™ 7 7700X",
    'https://portal.cherryservers.com/deployment?plan=780&tags=up_to_16': "AMD Ryzen™ 7950X"
}

@dp.message(Command("start"))
async def start_handler(message: Message):
    if message.chat.id not in user_chat_ids:
        user_chat_ids.add(message.chat.id)

# Словарь с флагами по странам
country_flags = {
    "Lithuania": "🇱🇹",
    "Netherlands": "🇳🇱",
    "United States": "🇺🇸",
    "Singapore": "🇸🇬"
}

async def check_server_status():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36")
        page = await context.new_page()

        while True:
            for url, server_name in url_to_server.items():
                try:
                    await page.goto(url, timeout=90000)
                    await page.wait_for_load_state("networkidle", timeout=90000)
                    #await asyncio.sleep(20)

                    # Инициализация текста сообщения только если есть серверы в наличии
                    message_text = ""

                    region_blocks = await page.query_selector_all(
                        "button.hover\\:border-zinc-300, button.border-blue-500")

                    for block in region_blocks:
                        # Извлекаем название региона
                        region_name_elem = await block.query_selector("div.text-sm.leading-snug.truncate")
                        if not region_name_elem:
                            region_name_elem = await block.query_selector("div.text-sm")

                        if region_name_elem:
                            region_name = await region_name_elem.inner_text()
                        else:
                            continue

                        # Извлекаем статус региона
                        status_elem = await block.query_selector("div.text-xs")
                        if status_elem:
                            status_text = await status_elem.inner_text()
                        else:
                            status_text = "Неизвестный статус"

                        quantity_elem = await block.query_selector("div.text-center > div.text-base")
                        if quantity_elem:
                            quantity_text = await quantity_elem.inner_text()
                        else:
                            quantity_text = "0"

                        # Извлекаем Литву из названия региона
                        country = region_name.split(",")[0]
                        if country == "Lithuania":
                            continue

                        flag = country_flags.get(country, "🏳️")

                        # Если сервер "In stock", добавляем информацию в сообщение
                        if "In stock" in status_text:
                            message_text += (
                                f"Cервера на процессоре {server_name} доступны в " f"{region_name}{flag}\n"                                
                                f"Количество серверов: {quantity_text}\n\n"
                                f"Можно купить по ссылке: {url}\n\n\n"
                            )

                    # Отправка сообщений пользователям, если есть доступные сервера
                    if message_text:
                        for chat_id in user_chat_ids:
                            await bot.send_message(
                                chat_id=chat_id,
                                text=message_text,
                                parse_mode="HTML"
                            )

                except Exception as e:
                    print(f"{datetime.now()}: Ошибка при проверке URL {url}: {e}")

            #Каждые 3 часа отправляет сообщение о статусе
            await asyncio.sleep(10800)


async def main():
    dp.message.register(start_handler)
    asyncio.create_task(check_server_status())
    await dp.start_polling(bot, skip_updates=True)


if __name__ == '__main__':
    asyncio.run(main())

import asyncio
from telegram_bot import run_telegram_bot

def main():
    loop = asyncio.get_event_loop()
    run_telegram_bot()
    loop.run_forever()

if __name__ == "__main__":
    main()

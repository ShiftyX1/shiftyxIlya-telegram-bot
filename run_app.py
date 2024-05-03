import gpt
import uvicorn
import multiprocessing
import asyncio


async def main():
    config = uvicorn.Config("admin:app", port=8000, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()


def run_web():
    asyncio.run(main())


def run_bot():
    asyncio.run(gpt.main())


async def start():
    bot = multiprocessing.Process(target=run_bot)
    admin_web = multiprocessing.Process(target=run_web)
    bot.start()
    admin_web.start()

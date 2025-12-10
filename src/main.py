import asyncio
from core.bot import Bot


async def main():
    async with Bot("argoars") as bot:
        await bot.farm_loop()


if __name__ == "__main__":
    asyncio.run(main())

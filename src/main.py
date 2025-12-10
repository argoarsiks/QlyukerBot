import asyncio
import sys

from core.bot import Bot
from core.config import settings
from utils.tg_session import create_session, get_all_sessions


async def parse_args(args: list):
    if args[1] == "--run":
        if len(args) > 2:
            session_name = args[2]

            if session_name == "all":
                sessions = get_all_sessions()

                await asyncio.gather(*[run_bot(session_name) for session_name in sessions])
            else:
                await run_bot(session_name)
        else:
            print("Specify session name or 'all'")
    else:
        print("Available commands: [--run]")


async def run_bot(session_name: str):
    async with Bot(session_name) as bot:
        await bot.farm_loop()


async def main():
    print("""    
░█████╗░██████╗░░██████╗░░█████╗░░█████╗░██████╗░░██████╗
██╔══██╗██╔══██╗██╔════╝░██╔══██╗██╔══██╗██╔══██╗██╔════╝
███████║██████╔╝██║░░██╗░██║░░██║███████║██████╔╝╚█████╗░
██╔══██║██╔══██╗██║░░╚██╗██║░░██║██╔══██║██╔══██╗░╚═══██╗
██║░░██║██║░░██║╚██████╔╝╚█████╔╝██║░░██║██║░░██║██████╔╝
╚═╝░░╚═╝╚═╝░░╚═╝░╚═════╝░░╚════╝░╚═╝░░╚═╝╚═╝░░╚═╝╚═════╝░
""")
    while True:
        print(
            "Select an option:\n1. Create new session\n2. Start session by name\n3. Start all sessions"  # noqa: E501
        )
        choice = int(input("Your choice: "))

        match choice:
            case 1:
                session_name = input("Enter a name for your session: ")
                await create_session(session_name, settings.api_id, settings.api_hash)
            case 2:
                session_name = input("Enter your session name: ")
                await run_bot(session_name)
            case 3:
                sessions = get_all_sessions()
                await asyncio.gather(*[run_bot(session_name) for session_name in sessions])


if __name__ == "__main__":
    if len(sys.argv) > 1:
        asyncio.run(parse_args(sys.argv))
    else:
        asyncio.run(main())

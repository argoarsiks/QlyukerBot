import os
import json
import asyncio
import argparse
from bot.core import mainLoop
from bot.utils import regSession


async def defConfig(sessionName):
    with open(f"{os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config', sessionName)}.json", "w", encoding="utf-8") as f:
        cfg = {
            "autoTaps": True,
            "autoUpgrade": True,
            "tapsPerCycle": "5;15",
            "sleep": "100;1000",
            "proxy": None
        }
        json.dump(cfg, f, ensure_ascii=False)


async def regSession():
    inpName = str(input("Enter a title for the session: "))
    resultReg = await regSession(sessionName=inpName)
    if resultReg == True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"Select a config:\n\n"
                f"1: Default config (legit)\n\n"
                f"2: Custom config\n")
        inpConfigChoice = int(input("Your choice: "))
        if inpConfigChoice == 1:
            await defConfig(inpName)
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"Config successfully saved (It can always be changed in the 'config' directory). To run the bot, restart the script")
        elif inpConfigChoice == 2:
            await defConfig(inpName)
            os.system('cls' if os.name == 'nt' else 'clear')
            config_path = f"{os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config', inpName)}.json"
            print(f"You can change the config along the way: {config_path}\n"
                    f"To run the bot, restart the script")


async def startBot():
    session_names = []
    for filename in os.listdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), "sessions")):
        if filename.endswith(".session"):
            session_names.append(os.path.splitext(filename)[0])
    tasks = [mainLoop(sessionName) for sessionName in session_names]
    await asyncio.gather(*tasks)


async def manualSetup():
    print("""   
██████╗░██╗░░░██╗  ░█████╗░██████╗░░██████╗░░█████╗░░█████╗░██████╗░░██████╗
██╔══██╗╚██╗░██╔╝  ██╔══██╗██╔══██╗██╔════╝░██╔══██╗██╔══██╗██╔══██╗██╔════╝
██████╦╝░╚████╔╝░  ███████║██████╔╝██║░░██╗░██║░░██║███████║██████╔╝╚█████╗░
██╔══██╗░░╚██╔╝░░  ██╔══██║██╔══██╗██║░░╚██╗██║░░██║██╔══██║██╔══██╗░╚═══██╗
██████╦╝░░░██║░░░  ██║░░██║██║░░██║╚██████╔╝╚█████╔╝██║░░██║██║░░██║██████╔╝
╚═════╝░░░░╚═╝░░░  ╚═╝░░╚═╝╚═╝░░╚═╝░╚═════╝░░╚════╝░╚═╝░░╚═╝╚═╝░░╚═╝╚═════╝░
          """)
    print(f"Select a mode:\n\n"
          f"1: Create a new session\n\n"
          f"2: Starting a bot\n")
    inp = int(input("Your choice: "))
    if inp == 1:
        await regSession()
    elif inp == 2:
        await startBot()


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--action", type=int, choices=[1,2], required=False)
    args = parser.parse_args()
    if args.action == 1:
        await regSession()
    elif args.action == 2:
        await startBot()
    else:
        await manualSetup()
                

if __name__ == "__main__":
    asyncio.run(main())
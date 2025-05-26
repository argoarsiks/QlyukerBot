import os
import sys
import time
import json
import random
import asyncio
import aiohttp
from pathlib import Path
from colorama import Fore, init

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from bot.utils import getTgWebApp
from bot.core.headers import headers

init()


async def loadCfg(sessionName):
    with open(f"{os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'config', sessionName)}.json", "r", encoding="utf-8") as f:
        return json.load(f)


async def login(session : aiohttp.ClientSession, sessionName):
    response = await session.post(url="https://api.qlyuker.io/auth/start", json={"startData": await getTgWebApp(sessionName)})
    if response.status == 200:
        data = await response.json()
        return data


async def sendTaps(session : aiohttp.ClientSession, taps, timeStart, startEnergy, energyPerSec):
    timeNow = int(time.time())
    currentEnergy = startEnergy + (timeNow - timeStart) * energyPerSec
    response = await session.post(url="https://api.qlyuker.io/game/sync", json={"clientTime": timeNow, "currentEnergy": currentEnergy, "taps": taps})
    if response.status == 200:
        data = await response.json()
        return data
    

async def buy(session : aiohttp.ClientSession, upgradeId):
    response = await session.post(url="https://api.qlyuker.io/upgrades/buy", json={"upgradeId": upgradeId})
    if response.status == 200:
        data = await response.json()
    else:
        data = {"error": True}
    return data


async def mainLoop(sessionName):
    while True:
        cfg = await loadCfg(sessionName)
        async with aiohttp.ClientSession(headers=headers, proxy=cfg["proxy"]) as session:
            loginData = await login(session, sessionName)
            timeStart = int(time.time())
            currentEnergy = int(loginData["game"]["currentEnergy"])
            energyPerSec = int(loginData["game"]["energyPerSec"])
            currentCoins = int(loginData["game"]["currentCoins"])
            currentTickets = int(loginData["game"]["currentTickets"])
            minePerHour = int(loginData["game"]["minePerHour"])
            upgrades = loginData["upgrades"]
            upgradesList = upgrades["list"]
            restoreEnergy = next(upgrade for upgrade in upgradesList if upgrade["id"] == "restoreEnergy")
            print(Fore.GREEN + f"[{sessionName}] Successfully launched")
            print(Fore.BLUE + f"[{sessionName}] Coins: {currentCoins}. Energy: {currentEnergy}, Tickets: {currentTickets}, Mine per hour: {minePerHour}")
            if cfg["autoTaps"] == True:
                minTaps, maxTaps = map(int, cfg["tapsPerCycle"].split(";"))
                if restoreEnergy["level"] != 6:
                    while currentEnergy >= 100:
                        await asyncio.sleep(random.randint(1, 5))
                        tapsData = await sendTaps(session, random.randint(minTaps, maxTaps), timeStart, currentEnergy, energyPerSec)
                        timeStart = int(time.time())
                        currentEnergy = tapsData["currentEnergy"]
                        currentCoins = tapsData["currentCoins"]
                        print(Fore.BLUE + f"[{sessionName}] Coins: {currentCoins}. Energy: {currentEnergy}, Tickets: {currentTickets}, Mine per hour: {minePerHour}")
                    statusBuy = await buy(session, "restoreEnergy")
                    if "error" not in statusBuy:
                        currentEnergy = 3000
                        while currentEnergy >= 100:
                            await asyncio.sleep(random.randint(1, 5))
                            tapsData = await sendTaps(session, random.randint(minTaps, maxTaps), timeStart, currentEnergy, energyPerSec)
                            timeStart = int(time.time())
                            currentEnergy = tapsData["currentEnergy"]
                            currentCoins = tapsData["currentCoins"]
                            print(Fore.BLUE + f"[{sessionName}] Coins: {currentCoins}. Energy: {currentEnergy}, Tickets: {currentTickets}, Mine per hour: {minePerHour}")
                else:
                    while currentEnergy >= 100:
                        await asyncio.sleep(random.randint(1, 5))
                        tapsData = await sendTaps(session, random.randint(minTaps, maxTaps), timeStart, currentEnergy, energyPerSec)
                        timeStart = int(time.time())
                        currentEnergy = tapsData["currentEnergy"]
                        currentCoins = tapsData["currentCoins"]
                        print(Fore.BLUE + f"[{sessionName}] Coins: {currentCoins}. Energy: {currentEnergy}, Tickets: {currentTickets}, Mine per hour: {minePerHour}")
            
            if cfg["autoUpgrade"] == True:
                for upgrade in upgradesList:
                    if upgrade["kind"] == "minePerHour":
                        statusBuy = await buy(session, upgrade["id"])
                        if "error" not in statusBuy:
                            print(Fore.BLUE + f"[{sessionName}] Buying {upgrade['id']}")
                            currentCoins = statusBuy["currentCoins"]
                            minePerHour = statusBuy["minePerHour"]
                            await asyncio.sleep(5)

        print(Fore.BLUE + f"[{sessionName}] Coins: {currentCoins}. Energy: {currentEnergy}, Tickets: {currentTickets}, Mine per hour: {minePerHour}")
        minSec, maxSec = map(int, cfg["sleep"].split(";"))
        sleepSec = random.randint(minSec, maxSec)
        print(Fore.RED + f"[{sessionName}] Sleeping for {sleepSec} seconds")
        await asyncio.sleep(sleepSec)
import asyncio
import random
import time
from utils.headers import headers
from core.config import settings
from utils.tg_session import get_web_app
import aiohttp


class Bot:
    def __init__(self, session_name: str):
        # Qlyuker
        self.coins_per_tap = None
        self.coins = None
        self.energy = None
        self.max_energy = None
        self.candies = None
        self.tickets = None
        self.energy_per_sec = None
        self.mine_per_sec = None
        self.last_sync = None

        self.session_name = session_name
        self.start_data = None
        self.session: aiohttp.ClientSession = None

        self.energy_lock = asyncio.Lock()
        self.coins_lock = asyncio.Lock()

    async def __aenter__(self):
        if self.session is None:
            self.session = aiohttp.ClientSession(
                base_url="https://qlyuker.sp.yandex.ru", headers=headers
            )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
            self.session = None

    async def _login(self) -> None:
        payload = {"startData": self.start_data}

        response = await self.session.post("api/auth/start", json=payload)

        if response.status == 200:
            response_data = await response.json()

            self.coins_per_tap = response_data["game"]["coinsPerTap"]
            self.candies = response_data["game"]["currentCandies"]
            self.coins = response_data["game"]["currentCoins"]
            self.energy = response_data["game"]["currentEnergy"]
            self.energy_per_sec = response_data["game"]["energyPerSec"]
            self.max_energy = response_data["game"]["maxEnergy"]
            self.mine_per_sec = response_data["game"]["minePerSec"]
            self.last_sync = int(time.time())

    async def _sync_request(self, taps: int) -> None:
        async with self.energy_lock:
            payload = {"clientTime": int(time.time()), "currentEnergy": self.energy, "taps": taps}

        response = await self.session.post("api/game/sync", json=payload)

        if response.status == 200:
            response_data = await response.json()

            async with self.energy_lock, self.coins_lock:
                self.candies = response_data["currentCandies"]
                self.coins = response_data["currentCoins"]
                self.energy = response_data["currentEnergy"]
                self.last_sync = response_data["lastSync"]

    async def _recovery_energy_task(self) -> None:
        while True:
            await asyncio.sleep(1)

            async with self.energy_lock:
                self.energy += self.energy_per_sec
                print(f"[Energy Task] Энергия восстановлена: {self.energy}/{self.max_energy}")
                print(f"[Stats] Монет: {self.coins}")

    async def _emulate_taps_task(self) -> None:
        while True:
            taps = random.randint(1, 51)
            clicks_per_second = random.randint(4, 9)

            async with self.energy_lock:
                self.energy -= taps * self.coins_per_tap

            await asyncio.sleep(taps / clicks_per_second)
            await self._sync_request(taps)

    async def _setup_bot(self) -> None:
        self.start_data = await get_web_app(self.session_name, settings.api_id, settings.api_hash)
        await self._login()

    async def farm_loop(self):
        await self._setup_bot()

        tasks = [
            asyncio.create_task(self._recovery_energy_task()),
            asyncio.create_task(self._emulate_taps_task()),
        ]

        await asyncio.gather(*tasks)

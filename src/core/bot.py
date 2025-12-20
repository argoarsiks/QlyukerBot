import asyncio
import random
import time

import aiohttp

from core.config import ConfigManager, settings
from utils.headers import headers
from utils.tg_session import get_web_app


class Bot:
    def __init__(self, session_name: str):
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

        self.lock = asyncio.Lock()
        self.is_running = False

        self.proxy = None

    async def __aenter__(self):
        if self.session:
            self.session = aiohttp.ClientSession(
                base_url="https://qlyuker.sp.yandex.ru",
                headers=headers,
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

            async with self.lock:
                self.coins_per_tap = response_data["game"]["coinsPerTap"]
                self.candies = response_data["game"]["currentCandies"]
                self.coins = response_data["game"]["currentCoins"]
                self.energy = response_data["game"]["currentEnergy"]
                self.energy_per_sec = response_data["game"]["energyPerSec"]
                self.max_energy = response_data["game"]["maxEnergy"]
                self.mine_per_sec = response_data["game"]["minePerSec"]
                self.last_sync = int(time.time())
                self.tickets = response_data["game"]["currentTickets"]

    async def _sync_request(self, taps: int) -> None:
        async with self.lock:
            payload = {"clientTime": int(time.time()), "currentEnergy": self.energy, "taps": taps}

        response = await self.session.post("api/game/sync", json=payload)

        if response.status == 200:
            response_data = await response.json()

            async with self.lock:
                self.candies = response_data["currentCandies"]
                self.coins = response_data["currentCoins"]
                self.energy = response_data["currentEnergy"]
                self.last_sync = response_data["lastSync"]
                self.tickets = response_data["currentTickets"]

    async def _buy_ticket_request(self) -> None:
        payload = {"count": 1}

        response = await self.session.post("api/game/tickets/buy", json=payload)

        if response.status == 200:
            response_data = await response.json()

            async with self.lock:
                self.candies = response_data["result"]["currentCandies"]
                self.tickets = response_data["result"]["currentTickets"]

    async def _recovery_energy_task(self) -> None:
        while self.is_running:
            await asyncio.sleep(1)

            async with self.lock:
                self.energy += self.energy_per_sec

    async def _emulate_taps_task(self) -> None:
        while self.is_running:
            is_sleep = False

            async with self.lock:
                if self.energy <= random.randint(200, 500):
                    is_sleep = True

            if is_sleep:
                await asyncio.sleep(5)
                continue

            taps = random.randint(1, min(51, self.energy // self.coins_per_tap))
            clicks_per_second = random.randint(4, 9)

            async with self.lock:
                self.energy -= taps * self.coins_per_tap

            await asyncio.sleep(taps / clicks_per_second)
            await self._sync_request(taps)

    async def _buy_tickets_task(self) -> None:
        while self.is_running:
            async with self.lock:
                can_buy = self.candies >= 10

            if can_buy:
                await self._buy_ticket_request()

            await asyncio.sleep(5)

    def _print_formatted(self, text: str, value=None) -> None:
        print(f"[{self.session_name}] {text} {value if value else ''}")

    async def _stats_task(self) -> None:
        while self.is_running:
            async with self.lock:
                self._print_formatted("Energy:", self.energy)
                self._print_formatted("Distance:", self.coins)
                self._print_formatted("Candies:", self.candies)
                self._print_formatted("Tickets:", self.tickets)
                self._print_formatted("Income per second:", self.mine_per_sec + 3)
                print("-" * 50)

            await asyncio.sleep(15)

    async def _restart_bot(self) -> None:
        await self._stop_tasks()
        await self.session.close()

        await self._update_session()

        await self._setup_bot()
        await self._start_tasks()

        self._print_formatted("Bot restarted")

    async def _restart_bot_task(self) -> None:
        while True:
            await asyncio.sleep(30 * 60)  # 30 minutes
            await self._restart_bot()

    async def _start_tasks(self) -> None:
        self.is_running = True

        self.tasks = [
            asyncio.create_task(self._recovery_energy_task()),
            asyncio.create_task(self._emulate_taps_task()),
            asyncio.create_task(self._buy_tickets_task()),
            asyncio.create_task(self._stats_task()),
        ]

    async def _stop_tasks(self) -> None:
        self.is_running = False

        for t in self.tasks:
            if not t.done():
                t.cancel()

        if self.tasks:
            await asyncio.gather(*self.tasks, return_exceptions=True)
        self.tasks.clear()

    async def _update_session(self) -> None:
        if self.session:
            await self.session.close()

        self.session = aiohttp.ClientSession(
            base_url="https://qlyuker.sp.yandex.ru", headers=headers, proxy=self.proxy
        )

    async def _setup_config(self) -> None:
        manager = ConfigManager()
        config = manager.load_config_by_profile(self.session_name)

        self.proxy = config.get("proxy")

        await self._update_session()

    async def _setup_bot(self) -> None:
        self.start_data = await get_web_app(self.session_name, settings.api_id, settings.api_hash)
        await self._setup_config()
        await self._login()

    async def farm_loop(self):
        await self._setup_bot()
        asyncio.create_task(self._restart_bot_task())
        await self._start_tasks()

        self._print_formatted("Bot started successfully!")

        try:
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            self._print_formatted("Bot stopped by user")

from pyrogram import Client
from pyrogram.raw.functions.messages import RequestWebView
from urllib.parse import urlparse, parse_qs, unquote
from pathlib import Path
import os

SESSION_DIR_PATH = Path(__file__).parent.parent.parent / "sessions"


def extract_tg_web_data(url: str) -> str:
    fragment = urlparse(url).fragment
    params = parse_qs(fragment)
    raw_data = unquote(params.get("tgWebAppData", [""])[0])
    return raw_data


async def get_web_app(sesion_name: str, api_id: int, api_hash: str) -> str:
    async with Client(sesion_name, api_id, api_hash, workdir=SESSION_DIR_PATH) as client:
        peer = await client.resolve_peer("qlyukerbot")
        web_view = await client.invoke(
            RequestWebView(
                peer=peer,
                bot=peer,
                platform="ios",
                from_bot_menu=False,
                url="https://qlyuker.sp.yandex.ru/front/",
            )
        )

    web_view_url = (web_view.url).replace("tgWebAppVersion=6.7", "tgWebAppVersion=9.1")
    return unquote(
        string=web_view_url.split("tgWebAppData=", maxsplit=1)[1].split(
            "&tgWebAppVersion", maxsplit=1
        )[0]
    )


async def create_session(session_name: str, api_id: int, api_hash: str) -> None:
    async with Client(session_name, api_id, api_hash, workdir=SESSION_DIR_PATH) as client:
        await client.get_me()


def get_all_sessions() -> list[str]:
    sessions = []

    for file in os.listdir(SESSION_DIR_PATH):
        if file.endswith("session"):
            sessions.append(file[:-8])

    return sessions

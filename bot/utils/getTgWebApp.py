from urllib.parse import urlparse, parse_qs, unquote
from pyrogram import Client
from pyrogram.raw.functions.messages import RequestWebView
from dotenv import load_dotenv
import os

load_dotenv()

SESSION_NAME = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "sessions", "my_session")


def extract_tg_web_data(url: str) -> str:
    fragment = urlparse(url).fragment
    params = parse_qs(fragment)
    raw_data = unquote(params.get('tgWebAppData', [''])[0])
    return parse_qs(raw_data).get("query_id", [""])[0]


async def getTgWebApp():
    API_ID = int(os.getenv("API_ID"))
    API_HASH = str(os.getenv("API_HASH"))

    async with Client(SESSION_NAME, API_ID, API_HASH) as app:
        peer = await app.resolve_peer("qlyukerbot")
        web_view = await app.invoke(
            RequestWebView(
                peer=peer,
                bot=peer,
                platform="ios",
                from_bot_menu=False,
                url="https://qlyuker.io/"
            )
        )
        tg_web_data = extract_tg_web_data(web_view.url)
        print(tg_web_data)
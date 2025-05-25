import os
from pyrogram import Client
from dotenv import load_dotenv
from pyrogram.errors import ApiIdInvalid, ApiIdPublishedFlood, AccessTokenInvalid, AccessTokenExpired

load_dotenv()


async def regSession(sessionName):
    try:
        API_ID = int(os.getenv("API_ID"))
        API_HASH = str(os.getenv("API_HASH"))
        SESSION_NAME = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "sessions", sessionName)
        app = Client(SESSION_NAME, API_ID, API_HASH)
        await app.start()
        me = await app.get_me()
        return True
    except (ApiIdInvalid, ApiIdPublishedFlood):
        print("Error: Incorrect API_ID or API_HASH")
    except (AccessTokenInvalid, AccessTokenExpired):
        print("Error: Incorrect or expired access token")
    return False
        
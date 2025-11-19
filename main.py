import os
import asyncio
from pyrogram import Client
from pyrogram.errors import ChannelInvalid, ChatAdminRequired, UserNotParticipant

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
SESSION = os.getenv("SESSION")

app = Client(
    "my_account",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION
)

CHANNEL_ID = -1002893284498  # your channel ID


async def join_live():
    await app.send_message("me", "🔄 Auto Live Join Script Started...")

    try:
        chat = await app.get_chat(CHANNEL_ID)

        if not chat.is_live_stream:
            await app.send_message("me", "❌ No live stream in this channel.")
            return

        await app.send_message("me", "🔗 Joining LIVE Stream…")
        await app.join_chat(CHANNEL_ID)

        await app.send_message("me", "✅ Successfully Joined LIVE Stream.")

    except UserNotParticipant:
        await app.join_chat(CHANNEL_ID)
        await join_live()

    except Exception as e:
        await app.send_message("me", f"⚠️ Error: {e}")


async def main():
    async with app:
        await join_live()
        await asyncio.Event().wait()   # KEEP RUNNING FOREVER


app.run(main())

import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from flask import Flask

# -----------------------------------------------------------------------------
# Telegram Credentials
# -----------------------------------------------------------------------------
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Channel IDs to monitor / auto join lives
CHANNEL_IDS = [
    -1002277022947,
    -1002352581494
]

# Pyrogram app
app = Client(
    "bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    workers=50
)

# -----------------------------------------------------------------------------
# FIRST FIX → Resolve Peer Error
# -----------------------------------------------------------------------------
async def resolve_all_channels():
    for cid in CHANNEL_IDS:
        try:
            await app.get_chat(cid)
            print(f"[OK] Resolved channel: {cid}")
        except Exception as e:
            print(f"[ERROR] Cannot resolve {cid}: {e}")

# -----------------------------------------------------------------------------
# AUTO JOIN LIVE STREAM FIXED
# -----------------------------------------------------------------------------
@app.on_message(filters.video_chat_started)
async def joined_live(_, msg: Message):
    try:
        await msg.reply("Bot joined live stream automatically!")
        print("[LIVE] Bot joined live.")
    except Exception as e:
        print(f"[ERROR LIVE] {e}")

# -----------------------------------------------------------------------------
# STARTUP
# -----------------------------------------------------------------------------
async def start_bot():
    await app.start()
    print("Bot started successfully.")

    await resolve_all_channels()  # IMPORTANT FIX

    print("All channels resolved. Bot is running.")
    await asyncio.Event().wait()  # replaces idle()

# -----------------------------------------------------------------------------
# Render Keep-Alive Web Server
# -----------------------------------------------------------------------------
server = Flask(__name__)

@server.route("/")
def home():
    return "Bot Running!"

# -----------------------------------------------------------------------------
# RUN EVERYTHING
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(start_bot())
    server.run(host="0.0.0.0", port=10000)

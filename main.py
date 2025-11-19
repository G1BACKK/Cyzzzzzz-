import os
import asyncio
from flask import Flask
from pyrogram import Client
from pyrogram.errors import PeerIdInvalid, ChatAdminRequired

# ----- Flask server (keeps Render alive) -----
app_flask = Flask(__name__)

@app_flask.route("/")
def home():
    return "Bot Running Successfully!"

# ----- Pyrogram Client -----
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
SESSION = os.getenv("SESSION")

CHANNEL_ID = -1002893284498   # your channel

app = Client("bot", api_id=API_ID, api_hash=API_HASH, session_string=SESSION)

async def auto_join_live():
    await app.start()
    print("⚡ Pyrogram Started Successfully!")

    while True:
        try:
            chat = await app.get_chat(CHANNEL_ID)

            if chat and chat.has_live_stream:
                print("🎥 Live detected… Joining…")
                await app.join_chat(CHANNEL_ID)
                print("✅ Joined Livestream!")
            else:
                print("⛔ No live stream right now")

        except PeerIdInvalid:
            print("❌ Invalid channel ID")
        except ChatAdminRequired:
            print("❌ You must join the channel yourself once manually")
        except Exception as e:
            print("⚠ Error:", e)

        await asyncio.sleep(10)   # checks every 10 sec

async def runner():
    await asyncio.gather(
        auto_join_live(),
    )

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(runner())

    app_flask.run(host="0.0.0.0", port=int(os.getenv("PORT", 10000)))

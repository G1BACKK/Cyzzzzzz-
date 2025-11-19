import os
import threading
import asyncio
from flask import Flask
from pyrogram import Client

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
SESSION = os.getenv("SESSION")

CHANNEL_ID = -1002893284498   # your channel

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot Running Successfully"

pyro = Client(
    "bot",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION,
    workers=1,            # FIX: must be minimum 1
    plugins=None,
    device_model="RenderServer",
    takeout=False,
)

async def join_live_loop():
    await pyro.start()
    print("🔥 Pyrogram Started")

    while True:
        try:
            chat = await pyro.get_chat(CHANNEL_ID)

            if getattr(chat, "has_live_stream", False):
                print("🎥 LIVE FOUND! Joining…")
                await pyro.join_chat(CHANNEL_ID)
                print("✅ Joined Live Stream")
            else:
                print("⛔ No live…")

        except Exception as e:
            print("❌ ERROR:", e)

        await asyncio.sleep(10)

def run_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_until_complete(join_live_loop())

loop = asyncio.new_event_loop()
threading.Thread(target=run_loop, args=(loop,), daemon=True).start()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

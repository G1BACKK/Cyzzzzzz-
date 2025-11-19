import os
import asyncio
from flask import Flask
from pyrogram import Client

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
SESSION = os.getenv("SESSION")

CHANNEL_ID = -1002893284498

app_flask = Flask(__name__)

@app_flask.route("/")
def home():
    return "Bot Running Successfully!"

pyro = Client(
    "bot",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION
)

async def auto_join_live():
    await pyro.start()
    print("🔥 Pyrogram Started")

    while True:
        try:
            chat = await pyro.get_chat(CHANNEL_ID)

            if chat.has_live_stream:
                print("🎥 Live detected! Joining…")
                await pyro.join_chat(CHANNEL_ID)
                print("✅ Joined livestream!")
            else:
                print("⛔ No live at the moment")

        except Exception as e:
            print("Error:", e)

        await asyncio.sleep(10)

async def start_all():
    task = asyncio.create_task(auto_join_live())
    await task

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(start_all())

    # Flask runs on main thread, Pyrogram runs in background
    app_flask.run(host="0.0.0.0", port=int(os.getenv("PORT", 10000)))

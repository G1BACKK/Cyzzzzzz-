import os
import threading
import asyncio
from flask import Flask
from pyrogram import Client

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
SESSION = os.getenv("SESSION")

CHANNEL_ID = -1002893284498

# Flask app
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot Running Successfully!"

# Pyrogram client
pyro = Client(
    "bot",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION
)

async def join_live_stream():
    await pyro.start()
    print("🔥 Pyrogram Started Successfully")

    while True:
        try:
            chat = await pyro.get_chat(CHANNEL_ID)

            if chat.has_live_stream:
                print("🎥 Live detected! Joining...")
                await pyro.join_chat(CHANNEL_ID)
                print("✅ Successfully Joined Live Stream!")
            else:
                print("⛔ No live currently…")

        except Exception as e:
            print("❌ Error:", e)

        await asyncio.sleep(10)

def start_async_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_until_complete(join_live_stream())

# Start Pyrogram in its own background thread
loop = asyncio.new_event_loop()
threading.Thread(target=start_async_loop, args=(loop,), daemon=True).start()

# Start Flask (main thread)
if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

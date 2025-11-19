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

CHANNEL_ID = -1002893284498     # put your channel ID here


async def join_live():
    await app.send_message("me", "🔄 Auto Live Join Script Started...")

    try:
        chat = await app.get_chat(CHANNEL_ID)

        if not chat.is_live_stream:
            await app.send_message("me", "❌ No live stream in this channel.")
            return

        # Get live stream chat ID
        live = await app.get_chat(chat.id)

        await app.send_message("me", "🔗 Joining Live Stream...")
        await app.join_chat(chat.id)

        await app.send_message("me", "✅ Successfully joined LIVE stream.")

    except UserNotParticipant:
        await app.send_message("me", "⚠️ You are not in the channel. Joining channel...")
        await app.join_chat(CHANNEL_ID)
        await join_live()

    except ChannelInvalid:
        await app.send_message("me", "❌ Invalid channel ID.")
    except ChatAdminRequired:
        await app.send_message("me", "❌ Need admin rights to join live.")
    except Exception as e:
        await app.send_message("me", f"⚠️ Error: {e}")


@app.on_message()
async def _(client, message):
    # Just to keep logs active
    print("Message:", message.text)


app.start()
app.loop.run_until_complete(join_live())
app.idle()

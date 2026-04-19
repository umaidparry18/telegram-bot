from telethon import TelegramClient, events
import re
import os
import asyncio

# ================== SECURE API ==================
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")

# ================== CHANNELS ==================
source_channels = [
    "intelslava",
    "DDGeopolitics",
    "Middle_East_Spectator",
    "RezistanceTrench1",
    "trtworld",
    "abc3213333"  # test channel
]

target_channel = "peak_insights_24x7"

# ================== CLIENT ==================
client = TelegramClient("railway_session", api_id, api_hash)

# ================== TEXT CLEANING ==================
def clean_text(text):
    if not text:
        return ""

    text = re.sub(r"http\S+", "", text)   # remove links
    text = re.sub(r"@\w+", "", text)      # remove usernames
    text = re.sub(r"^[^\w]+", "", text)   # remove starting emojis/symbols
    text = re.sub(r"\n\s*\n", "\n\n", text)

    text = text.replace("BREAKING", "Latest Update")
    text = text.replace("Breaking", "Latest Update")

    text += "\n\n@peak_insights_24x7"

    return text.strip()

# ================== HANDLER ==================
@client.on(events.NewMessage(chats=source_channels))
async def handler(event):
    try:
        msg = event.message.message or ""

        if msg or event.message.media:
            new_text = clean_text(msg)

            await client.send_message(
                target_channel,
                new_text if new_text else "Latest Update\n\n@peak_insights_24x7",
                file=event.message.media
            )

    except Exception as e:
        print("Handler error:", e)

# ================== MAIN LOOP ==================
async def main():
    while True:
        try:
            await client.start()
            print("✅ Bot running on Railway...")
            await client.run_until_disconnected()
        except Exception as e:
            print("⚠️ Restarting due to error:", e)
            await asyncio.sleep(5)


asyncio.run(main())
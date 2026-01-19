import os, json
from telethon import TelegramClient
from telethon.tl.types import MessageMediaPhoto
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

API_ID = int(os.getenv("TELEGRAM_API_ID"))
API_HASH = os.getenv("TELEGRAM_API_HASH")

CHANNELS = [
    "CheMed",
    "lobelia4cosmetics",
    "tikvahpharma"
]

client = TelegramClient("session", API_ID, API_HASH)

async def main():
    await client.start()

    today = datetime.today().strftime("%Y-%m-%d")
    msg_dir = f"data/raw/telegram_messages/{today}"
    img_dir = "data/raw/images"

    os.makedirs(msg_dir, exist_ok=True)
    os.makedirs(img_dir, exist_ok=True)

    for channel in CHANNELS:
        print(f"Scraping {channel}")
        os.makedirs(f"{img_dir}/{channel}", exist_ok=True)
        messages = []

        async for msg in client.iter_messages(channel, limit=300):
            record = {
                "message_id": msg.id,
                "channel_name": channel,
                "message_date": msg.date.isoformat() if msg.date else None,
                "message_text": msg.text,
                "views": msg.views,
                "forwards": msg.forwards,
                "has_media": False,
                "image_path": None
            }

            if isinstance(msg.media, MessageMediaPhoto):
                path = f"{img_dir}/{channel}/{msg.id}.jpg"
                await client.download_media(msg.media, path)
                record["has_media"] = True
                record["image_path"] = path

            messages.append(record)

        with open(f"{msg_dir}/{channel}.json", "w", encoding="utf-8") as f:
            json.dump(messages, f, indent=2, ensure_ascii=False)

        print(f"Saved {len(messages)} messages")

    await client.disconnect()

import asyncio
asyncio.run(main())

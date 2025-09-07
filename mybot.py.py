import asyncio
from telethon import TelegramClient, events
from telethon.tl.functions.messages import GetHistoryRequest

# =======================
# তোমার API ID & HASH
# =======================
api_id = ---------
api_hash = "----------"

# =======================
# সোর্স এবং ডেস্ট গ্রুপ আইডি
# =======================
SOURCE_GROUP_ID = -------   # সোর্স গ্রুপ
DEST_GROUP_ID   =-------   # ডেস্টিনেশন গ্রুপ

# =======================
# TelegramClient তৈরি
# =======================
client = TelegramClient("session", api_id, api_hash)

# =======================
# পুরানো ভিডিও ফরোয়ার্ড ফাংশন
# =======================
async def forward_old_videos(source, dest, batch_limit=100):
    print("⏳ পুরানো ভিডিওগুলো নিচ্ছে...")
    offset_id = 0
    total_count = 0

    while True:
        history = await client(GetHistoryRequest(
            peer=source,
            limit=batch_limit,
            offset_id=offset_id,
            offset_date=None,
            max_id=0,
            min_id=0,
            add_offset=0,
            hash=0
        ))

        messages = history.messages
        if not messages:
            break

        for msg in messages:
            if msg.video:
                await client.forward_messages(dest, msg)
                total_count += 1
                await asyncio.sleep(1)  # ছোট delay, rate-limit এড়াতে

        offset_id = messages[-1].id

    print(f"✅ সব ভিডিও ফরোয়ার্ড হয়েছে। মোট: {total_count}")

# =======================
# নতুন ভিডিও হ্যান্ডলার
# =======================
@client.on(events.NewMessage(chats=SOURCE_GROUP_ID))
async def new_video_handler(event):
    if event.message.video:
        await client.forward_messages(DEST_GROUP_ID, event.message)
        print("📹 নতুন ভিডিও ফরোয়ার্ড হয়েছে।")

# =======================
# মেইন ফাংশন
# =======================
async def main():
    source = await client.get_entity(SOURCE_GROUP_ID)
    dest   = await client.get_entity(DEST_GROUP_ID)

    # পুরানো ভিডিও ফরোয়ার্ড
    await forward_old_videos(source, dest)

    print("🤖 বট চালু আছে, নতুন ভিডিও অটো ফরোয়ার্ড হবে...")
    await client.run_until_disconnected()

# =======================
# স্ক্রিপ্ট রান
# =======================
with client:
    client.loop.run_until_complete(main())


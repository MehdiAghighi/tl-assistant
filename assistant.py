from telethon import TelegramClient, events, types, functions, sync
import socks
from dotenv import load_dotenv
import os
import logging

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)

# Loading Environment varriables
load_dotenv()

api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')

client = TelegramClient(
    'Assistant',
    api_id,
    api_hash,
    proxy=(socks.SOCKS5, '127.0.0.1', 8383) if os.getenv(
        'USE_PROXY') == "TRUE" else False
)


@events.register(events.NewMessage(outgoing=True, func=lambda event: event.raw_text.startswith('!!')))
async def newMessageSent(event):
    await client.delete_messages(event.chat_id, event.id)
    command = event.raw_text[2:]
    user = await event.get_chat()
    if command == 'id':
        if event.is_private:
            await client.send_message("me", "[" + user.first_name + "]" + "(" + "https://t.me/" + user.username + ")" + " : " + "`" + str(user.id) + "`", link_preview=False)
        if event.is_reply:
            replyed_message = await event.get_reply_message()
            replyed_user = await client.get_entity(replyed_message.from_id)
            await client.send_message("me", "[" + replyed_user.first_name + "]" + "(" + "https://t.me/" + replyed_user.username + ")" + " : " + "`" + str(replyed_user.id) + "`", link_preview=False)


@events.register(events.MessageRead(func=lambda e: e.is_private))
async def messageRead(event):
    user = await event.get_chat()
    message = await client.get_messages(user, ids=event.max_id)
    await client.send_message("me", "[" + user.username.capitalize() + "]" + "(" + "https://t.me/" + user.username + ")" + " Has Read My Message " + "👇", link_preview=False)
    await message.forward_to("me")

client.start()
client.add_event_handler(newMessageSent)
client.add_event_handler(messageRead)
client.run_until_disconnected()

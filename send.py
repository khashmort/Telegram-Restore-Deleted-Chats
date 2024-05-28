from telethon import TelegramClient
from telethon.tl.types import PeerChat
import json
import time
import glob
from datetime import datetime


# Remember to use your own values from my.telegram.org!
api_id = 28871117
api_hash = 'f1c54c6743805b47c890aa1732be9f1e'
client = TelegramClient('anon', api_id, api_hash)

async def main():

    chat_id = 2129610679
    entity = await client.get_entity(chat_id)
    
    with open("dump.json", "r") as file:
        content = json.load(file)
    
        did_send_media_msg = False

        for i, msg in enumerate(content):
            message_id = msg.get("id")
            message = msg.get("message", "")
            has_media = msg.get('media') is not None
            # media = msg.get('media',None)
            # webpage = media.get('webpage',None)
            # display_url = webpage.get('display_url',False)
                
            date = datetime.fromisoformat(msg.get("date", "")).strftime("%Y %b %d, %H:%M")

            # Print message, date, and attachment info:
            print(f"{i} {message}, {date}, has_media: {has_media}")

            if message:
                message = f"{date}\n\n{message}"
            else:
                message = str(date)

            if has_media:
                file_names = glob.glob(f"{message_id}.*")
                if (file_names):
                    for file_name in file_names:
                        print(f"Sending Media: {file_name}")
                        await client.send_file(entity, file_name,caption=message)
                         # client.send_file(entity=group, file=file_name, caption=message, silent=True)
                        did_send_media_msg = True
                else:
                    await client.send_message(entity, message)
            if not message:
                print('OUT')
                break
            elif message:
                print(f"Sending Message: {message}")
                await client.send_message(entity, message.encode('unicode-escape').decode('unicode-escape'))

            # Sleep to avoid rate limiting, you may experiment with reducing this time:
            time.sleep(2)



with client:
    client.loop.run_until_complete(main())
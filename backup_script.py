
from telethon import TelegramClient, events, sync
from telethon.tl.types import InputChannel, PeerChannel
from telethon.tl.types import Channel
import time

# Get your own api_id and
# api_hash from https://my.telegram.org, under API Development.
#  or from https://tjhorner.dev/webogram/#/login
api_id = 28871117
api_hash = 'f1c54c6743805b47c890aa1732be9f1e'
group_id= 1728252192
client = TelegramClient('session_name', api_id, api_hash)
client.start()

group = client.get_entity(PeerChannel(int(group_id)))

#messages = client.get_admin_log(group)

file1 = open("dump.json","w") 
c = 0
m = 0
for event in client.iter_admin_log(group):
    if event.deleted_message:
        print("Dumping message",c, "(", event.old.id, event.old.date,")")
        file1.write(event.old.to_json() + ",") 
        c+=1
        if event.old.media:
            m+=1
            #print(event.old.media.to_dict()['Document']['id'])
            client.download_media(event.old.media, str(event.old.id))
            print(" Dumped media", m)
        time.sleep(0.1)

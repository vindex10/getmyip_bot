import telepot
import ipgetter
import time
import urllib3
import sys
import json


with open("config.json", "r") as fin:
    cfg = json.load(fin)

chids=cfg["chids"]

def runloop(chids, initmsg=None):
    bot = telepot.Bot(cfg["bot_hash"])

    if initmsg:
        for chid in chids:
            bot.sendMessage(chid, initmsg)

    def handle(msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        print(content_type, chat_type, chat_id)
        sys.stdout.flush()

        if content_type == 'text' and msg["text"] == "ip" and chat_id in chids:
            try:
                ip = ipgetter.myip()
                bot.sendMessage(chat_id, "Here is your ip '{}'".format(ip))
            except:
                bot.sendMessage(chat_id, "Failed to get ip")


    bot.message_loop(handle)

    print ('Listening ...')

    # Keep the program running.
    while 1:
        time.sleep(10)

if __name__ == "__main__":
    msg = "Awake!"

    while 1:
        try:
            runloop(chids, msg)
        except urllib3.exceptions.MaxRetryError:
            time.sleep(10)

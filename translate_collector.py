import time
from pytchat import LiveChat
a=input('link:')
if 'youtube' in a:livechat = LiveChat(a)
else:livechat = LiveChat(video_id = a)
t=time.time()

def condition(s,n):
    if n.name=='Fah':
        return True         #if there is a usual translator you can input there name here
    if '[en]' in s or '[EN]' in s:
        return True         #some time they will translate as"[EN]:she is talking about..."
    if n.isVerified:
        return True         #check if there is some channel comment?if its japanese you can use translate with in https://github.com/fah-OwO/realtime-auto-translate-using-clipboard/blob/master/autotranslate.py
    if s.count(':')==1:
        return True         #some time it will be like "subaru:she is talking about" and I use count as 1 because there will be emoticon like :":_ナンバー1:" or ":_にこにこ:"
    return False            #you can add case condition by your self
print('start with - to show that this application is running (it will appear every 5 seconds)")
print("start with > to show that those message match translate message condition")
while livechat.is_alive():
    try:
        chatdata = livechat.get()
        for c in chatdata.items:
            if condition(c.message,c.author):
                print(f" > {c.message}")
                t=time.time()
            elif 'a' in c.message and time.time()-t >=5:
                print(f"- {c.message}")
                t=time.time()
            chatdata.tick()
    except KeyboardInterrupt:
        livechat.terminate()
        break

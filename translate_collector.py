from pytchat import LiveChat
a=input('link:')
if 'youtube' in a:livechat = LiveChat(a)
else:livechat = LiveChat(video_id = a)

def condition(s,n):
    if n.name=='Fah':
        return True         #if there is a usual translator you can input there name here
    z=s.lower()
    if 'en]' in z or '[en' in z or u'【en' in z or u'(en' in z or 'talking about' in z:
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
            chatdata.tick()
    except KeyboardInterrupt:
        livechat.terminate()
        break

print("live chat end")
input("press enter to exit")

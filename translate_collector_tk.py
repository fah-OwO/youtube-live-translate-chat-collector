import time
import tkinter as tk
from pytchat import LiveChat
import codecs
import threading
def condition(s,n):
    if n.name=='Catsy':
        return True         #if there is a usual translator you can input there name here
    if '[en]' in s or '[EN]' in s:
        return True         #some time they will translate as"[EN]:she is talking about..."
    if n.isVerified:
        return True         #check if there is some channel comment?if its japanese you can use translate with in https://github.com/fah-OwO/realtime-auto-translate-using-clipboard/blob/master/autotranslate.py
    if s.count(':')==1:
        return True         #some time it will be like "subaru:she is talking about" and I use count as 1 because there will be emoticon like :":_ナンバー1:" or ":_にこにこ:"
    return False            #you can add case condition by your self

    
class collector(threading.Thread):
    def __init__(self,link):
        super(collector,self).__init__()
        if 'youtube' in a:self.livechat = LiveChat(link)
        else:self.livechat = LiveChat(video_id = link)
        self.program_running=True
        # self.t=time.time()
        

    def exit(self):
        self.running=False
        self.program_running=False

    def run(self):
        global d,data,lastdata
        while self.livechat.is_alive():
            if not self.program_running:
                self.livechat.terminate()
                break
            try:
                self.chatdata = self.livechat.get()
                for c in self.chatdata.items:
                    if condition(c.message,c.author):
                        d=f" > {c.author.name}\n{c.message}\n\n"
                        print(d)
                    #     self.t=time.time()
                    # elif 'a' in c.message and time.time()-self.t >=5:
                    #     print(f"- {c.message}")
                    #     self.t=time.time()
                    self.chatdata.tick()
            except KeyboardInterrupt:
                self.livechat.terminate()
    
a=input('link:')
d=''
data=''
lastdata=''
clt=collector(a)
clt.start()
def tkloop():
    global d,data,lastdata
    data=d
    if lastdata!=data:
        text.insert(1.0,data)
    lastdata=data
    text.after(50, tkloop)

root = tk.Tk()
root.title("translate collector")
root.attributes("-topmost", True)
root.bind('<Escape>', lambda e: root.quit())
text = tk.Text(root,height=20,width=30,font="Sans 24",padx=20,pady=10)
text.pack()
tkloop()
root.mainloop()
clt.exit()

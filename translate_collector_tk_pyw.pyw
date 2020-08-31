import time
import tkinter as tk
from pytchat import LiveChat
import codecs
import threading

emoji='[ ] ( ) < >'.split()+[str(i) for i in range(10)]
member=['Catsy' , 'Fah' ]         #if there is a usual translator you can input there name here
def condition(s,n):
    z=s.lower()
    if 'en]' in z or '[en' in z or u'【en' in z or u'(en' in z or 'talking about' in z:
        return f"{s}\n\n"                       #some time they will translate as"[EN]:she is talking about..."
    if n.isVerified:
        return f" > {n.name}\n{s}\n\n"          #check if there is some channel comment?if its japanese you can use translate with in https://github.com/fah-OwO/realtime-auto-translate-using-clipboard/blob/master/autotranslate.py
    for i in member:
        if n.name==i:return f" > {n.name}\n{s}\n\n"
    if s.count(':')==1:
        a=s.find(":")
        if len(s)-a<=3:return False
        if z[a:a+3]in [': 3',':ze']:return False
        if s[a+1] not in emoji:
            return f"{s}\n\n"                   #some time it will be like "subaru:she is talking about" and I use count as 1 because there will be emoticon like :":_ナンバー1:" or ":_にこにこ:"
    return False                                #you can add case condition by your self

maintranslator={}
def maintranslatoradd(st):
    if st in maintranslator:
        maintranslator[st]+=1
    else:
        maintranslator[st]=1

    
class collector(threading.Thread):
    def __init__(self):
        super(collector,self).__init__()
        self.livechat=''
        self.program_running=True
        self.running=False
        # self.t=time.time()
        
    def setlink(self,link):
        if 'youtube' in link:self.livechat = LiveChat(link)
        else:self.livechat = LiveChat(video_id = link)
        self.running=True

    def exit(self):
        self.running=False
        self.program_running=False

    def run(self):
        while self.program_running:
            while self.running:
                while self.livechat.is_alive():
                    if self.program_running:
                        try:
                            try:self.chatdata = self.livechat.get()
                            except:break
                            for c in self.chatdata.items:
                                d=condition(c.message,c.author)
                                if d:
                                    sendertext.insert(1.0,f"[ >{c.author.name}]")
                                    maintranslatoradd(c.author.name)
                                    text.insert(1.0,d)
                                self.chatdata.tick()
                        except KeyboardInterrupt:
                            self.livechat.terminate()
                else:
                    break
            time.sleep(0.1)
        return True
    
clt=collector()
clt.start()
def start():
    
    try:
        a= linktext.get("1.0",'end-1c')
        text.insert(1.0,'collecting\n > '+ a+'\n')
        clt.setlink(a)
    except Exception as e:
        print(e)
    
root = tk.Tk()
root.title("translate collector")
root.attributes("-topmost", True)
root.bind('<Escape>', lambda e: root.quit())
text = tk.Text(root,height=18,width=30,font="Sans 24",padx=30,pady=30)
text.grid(row=0,columnspan=20)
senderlabel = tk.Label(root,height=1,width=8,font="Sans 15",text='Sender:')
senderlabel.grid(row=1,columnspan=4)
sendertext = tk.Text(root,height=1,width=40,font="Sans 15",padx=20,pady=10)
sendertext.grid(row=1, column=4,columnspan=16)
textbutton=tk.Button(text="clear screen",command=lambda : text.delete(1.0,tk.END),width=60,font="Sans 12",padx=30,pady=10)
textbutton.grid(row=2,columnspan=20)
linktext = tk.Text(root,height=1,width=40,font="Sans 15",padx=20,pady=10)
linktext.grid(row=3, column=0,columnspan=16)
linkbutton=tk.Button(text="ok",command=start,font="Sans 15",width=8)
linkbutton.grid(row=3, column=16,columnspan=4)
root.mainloop()
for i,j in maintranslator.items():
    print(i,':',j)
clt.exit()

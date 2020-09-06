import time
import tkinter as tk
from pytchat import LiveChat
import codecs
import threading
import datetime
import googletrans as gt
translator = gt.Translator()
keyword={'talking about'}
member={'Fah','サトウスズキ'}                  #if there is a usual translator you can input there name here
emoji='[ ] ( ) < >'.split()+[str(i) for i in range(10)]
def condition(s,n):
    z=s.lower()
    a=z.find('en')
    if a>0:
        if z[a-1]in '[【(' or z.find(']',a)>a:
            return f"{s}\n\n" 
    if  any(word in s for word in keyword):
        return f"{s}\n\n"                       #some time they will translate as"[EN]:she is talking about..."
    if n.isVerified:                            #eg. "Subaru Ch. 大空スバル​あじ！"
        en=translator.translate(s,dest="en")
        if en.src=='en':return f" > {n.name}\n{s}\n\n"          
        else:return f" > {n.name}\n{s}\nTranslate from{en.src}\n{en.text}\n\n" 
    if any(name ==n.name for name in member):return f" > {n.name}\n{s}\n\n"
    a=s.find(":")
    if a!=-1 and s.find(":",a)==-1:
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
                                    maintranslatoradd(c.author.name)
                                    sendertext.insert(1.0,f"[ >{c.author.name} ({maintranslator[c.author.name]})]")
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
        text.insert(1.0,e)

def addkeywordbutton(root,row,columnspan):
    column=columnspan
    entertext=tk.Text(root,height=1,width=16,font="Sans 15")
    entertext.grid(row=row,column=column*2,columnspan=columnspan*2)
    def duty(set,mode,setname):
        a=entertext.get("1.0",'end-1c')
        s=mode+' '+setname+': "'+ a+'"'
        if 'add' ==mode:
            if a in set:s='"'+a+'" already in '+setname
            else:set.add(a)
        elif 'remove' ==mode:
            if a in set:set.remove(a)
            else:s='no "'+a+'" in'+setname# text.insert(1.0,'no '+a+' in '+string.replace('remove',''))
        text.insert(1.0,s+'\n'+setname+' now :\n'+str(set)+'\n\n')
    
    addkeyword=tk.Button(text="add key word",command=lambda:duty(keyword,'add','key word'),font="Sans 10",width=12)
    addkeyword.grid(row=row,column=0,columnspan=columnspan)
    addname=tk.Button(text="add member",command=lambda:duty(member,'add','member'),font="Sans 10",width=12)
    addname.grid(row=row,column=column,columnspan=columnspan)
    removekeyword=tk.Button(text="remove key word",command=lambda:duty(keyword,'remove','key word'),font="Sans 10",width=12)
    removekeyword.grid(row=row,column=column*4,columnspan=columnspan)
    removename=tk.Button(text="remove member",command=lambda:duty(member,'remove','member'),font="Sans 10",width=12)
    removename.grid(row=row,column=column*5,columnspan=columnspan)
    

root = tk.Tk()
root.title("translate collector")
root.attributes("-topmost", True)
root.bind('<Escape>', lambda e: root.quit())
text = tk.Text(root,height=18,width=30,font="Sans 24",padx=30,pady=30)
text.grid(row=0,columnspan=20)
linktext = tk.Text(root,height=1,width=40,font="Sans 15",padx=20,pady=10)
linktext.grid(row=3, column=0,columnspan=16)
linkbutton=tk.Button(text="ok",command=start,font="Sans 15",width=8)
linkbutton.grid(row=3, column=16,columnspan=4)

addkeywordbutton(root,2,3)
senderlabel = tk.Label(root,height=1,width=10,font="Sans 8",text='Sender:')
senderlabel.grid(row=1,columnspan=4)
sendertext = tk.Text(root,height=1,width=80,font="Sans 8")
sendertext.grid(row=1, column=4,columnspan=16)

root.mainloop()
clt.exit()
# textbutton=tk.Button(text="clear screen",command=lambda : text.delete(1.0,tk.END),width=60,font="Sans 12",padx=30,pady=10)
# textbutton.grid(row=2,columnspan=20)

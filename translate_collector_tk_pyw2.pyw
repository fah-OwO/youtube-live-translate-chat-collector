import time
import tkinter as tk
from pytchat import LiveChat
from threading import Thread as thr
from googletrans import Translator as gt

# if you dont want this window to be on top delete this line: "root.attributes("-topmost", True) "

# how to use :run this and put link on lowest tab and click ok
# (optional) you can add temporary keyword ore favorite translate by using middle tab and click add keyword/member button
# (can edit in code) there will be "sender:" tab which show sender and sending counting
# good luck and welcome to rabbit hole (kusa)

starttime=time.time()
translator = gt()
keyword={'talking about'}
member=set()                                    # if there is a usual translator you can input there name here
emoji='[',']' ,'(' ,')' ,'<' ,'>','0','1','2','3','4','5','6','7','8','9'       # add this to avoid catching sentence with ':'  some say "it's 12:30 pm  right now" or "sadddddd :["
def condition(s,n):
    def t(s,n):                         #return translate if it is not english language
        tmp='en'                           
        try:
            en=translator.translate(s,dest="en")
            tmp=en.src
        except: return f" > {n.name}\n{s}"  
        if tmp=='en':return f" > {n.name}\n{s}"          
        else:return f" > {n.name}\n{s}\n{en.text}" 
    z=s.lower()
    a=z.find('en')
    if a>0 and any(z.rfind(char1,0,a)!=-1 and z.find(char2,a)!=-1 for char1,char2 in zip('[(【','])】')) :
            return s                    # if [en] 【en】(en) or [smth/en]
    if  any(word in s for word in keyword):
        return s                         # some time they will translate as"[EN]:she is talking about..."
    if n.isVerified:                     # eg. "Subaru Ch. 大空スバル​あじ！"
        return t(s,n)
    if any(name ==n.name for name in member):
        return t(s,n)
    a=s.find(":")                       # some time it will be like "subaru:she is talking about" and I use count as 1 because there will be emoticon like :":_ナンバー1:" or ":_にこにこ:"
    if a!=-1 and s.find(":",a+1)==-1:   # if you cant hnadle this just delete it
        if len(s)-a<=3:return False
        elif z[a:a+3]in (': 3',':ze'):return False
        elif s[a+1] not in emoji:return s                   
    return False                        # you can add case condition by your self

maintranslator={}
def maintranslatoradd(st):
    if st in maintranslator:maintranslator[st]+=1
    else:maintranslator[st]=1
    
class collector(thr):
    def __init__(self):
        super(collector,self).__init__()
        self.livechat=False
        self.program_running=True
        self.running=False
        
        
    def setlink(self,link):
        if self.livechat:self.livechat.terminate()
        self.livechat = LiveChat(link)
        self.running=True

    def exit(self):
        if self.livechat:self.livechat.terminate()
        self.running=False
        self.program_running=False

    def run(self):
        while self.program_running:
            while self.running and self.livechat.is_alive():
                try:
                    self.chatdata = self.livechat.get()
                    for c in self.chatdata.items:
                        if not self.running:break
                        d=condition(c.message,c.author)
                        if d:
                            maintranslatoradd(c.author.name)
                            sendertext.insert(1.0,f"[ >{c.author.name} ({maintranslator[c.author.name]})]")
                            text.insert(1.0,d+'\n\n')
                            pos = '{}+{}c'.format('1.0', len(d))
                            text.tag_add('black','1.0',pos)
                        self.chatdata.tick()
                except KeyboardInterrupt:
                    self.livechat.terminate()
                    break
            time.sleep(0.1)
    
clt=collector()
clt.start()
def start():
    try:
        a= linktext.get("1.0",'end-1c')
        text.insert(1.0,'collecting\n > '+ a+'\n')
        clt.setlink(a)
    except Exception as e:
        print(e)

def addkeywordbutton(root,row,columnspan):
    column=columnspan
    entertext=tk.Text(root,height=1,width=16,font="Sans 15")
    entertext.grid(row=row,column=column*2,columnspan=columnspan*2)
    ds={'key word':keyword,'member':member}
    def duty(mode,setname):
        set=ds[setname]
        a=entertext.get("1.0",'end-1c')
        s=mode+' '+setname+': "'+ a+'"'
        if 'add' ==mode:
            if a in set:s='"'+a+'" already in '+setname
            else:set.add(a)
        elif 'remove' ==mode:
            if a in set:set.remove(a)
            else:s='no "'+a+'" in'+setname
        text.insert(1.0,s+'\n'+setname+' now :\n'+str(set)+'\n\n')
    
    addkeyword=tk.Button(text="add key word",command=lambda:duty('add','key word'),font="Sans 10",width=12)
    addkeyword.grid(row=row,column=0,columnspan=columnspan)
    addname=tk.Button(text="add member",command=lambda:duty('add','member'),font="Sans 10",width=12)
    addname.grid(row=row,column=column,columnspan=columnspan)
    removekeyword=tk.Button(text="remove key word",command=lambda:duty('remove','key word'),font="Sans 10",width=12)
    removekeyword.grid(row=row,column=column*4,columnspan=columnspan)
    removename=tk.Button(text="remove member",command=lambda:duty('remove','member'),font="Sans 10",width=12)
    removename.grid(row=row,column=column*5,columnspan=columnspan)
    
transparentcolor="grey"
root = tk.Tk()
root.title("translate collector")
root.bind('<Escape>', lambda e: root.quit())
root.attributes("-topmost", True)                                   #always on top of all window
try:                                                                #try invisible it
    root.wait_visibility(root)
    root.wm_attributes('-alpha',0.9)
    root.attributes("-transparentcolor", transparentcolor)
    text = tk.Text(root,height=18,width=30,font="Sans 24",padx=30,pady=30,background=transparentcolor,foreground="white")
    text.tag_config('black', background='black')
except:
    print(" can't invisible tkinter ,maybe because of your device os ")
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
print("time:",time.time()-starttime)
for i,j in maintranslator.items():
    print(i,':',j)
clt.exit()

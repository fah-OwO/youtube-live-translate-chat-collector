# import time
from time import sleep
import tkinter as tk
from pytchat import LiveChat
from threading import Thread as thr
from googletrans import Translator as gt
translator = gt()
keyword={'talking about'}
member=set()
emoji='[',']' ,'(' ,')' ,'<' ,'>','0','1','2','3','4','5','6','7','8','9'
def condition(s,n):
    def t(s,n):
        tmp='en'                           
        try:
            en=translator.translate(s,dest="en")
            tmp=en.src
        except: return f" > {n.name}\n{s}\n\n"  
        if tmp=='en':return f" > {n.name}\n{s}\n\n"          
        else:return f" > {n.name}\n{s}\n{en.text}\n\n" 
    z=s.lower()
    a=z.find('en')
    if a>0:
        if any(z.rfind(char1,0,a)!=-1 and z.find(char2,a)!=-1 for char1,char2 in zip('[(【','])】')) :
            return f"{s}\n\n" 
    if  any(word in s for word in keyword):
        return f"{s}\n\n"                       
    if n.isVerified:
        return t(s,n)
    if any(name ==n.name for name in member):
        return t(s,n)
    a=s.find(":")
    if a!=-1 and s.find(":",a+1)==-1:
        if len(s)-a<=3:return False
        if z[a:a+3]in (': 3',':ze'):return False
        if s[a+1] not in emoji:
            return f"{s}\n\n"                   
    return False                                

maintranslator={}
def maintranslatoradd(st):
    if st in maintranslator:
        maintranslator[st]+=1
    else:
        maintranslator[st]=1
    
class collector(thr):
    def __init__(self):
        super(collector,self).__init__()
        self.livechat=''
        self.program_running=True
        self.running=False
        
        
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
                                    print(f"[ >{c.author.name} ({maintranslator[c.author.name]})]")
                                    print(d)
                                    
                                self.chatdata.tick()
                        except KeyboardInterrupt:
                            self.livechat.terminate()
                else:
                    break
            sleep(0.1)
        return True
    
clt=collector()
clt.start()
def start(a):
    
    try:
        a= a
        print('collecting\n > '+ a+'\n')
        clt.setlink(a)
    except Exception as e:
        print(e)

# def addkeyword():
ds={'key word':keyword,'member':member}
def duty(a,mode='add',setname='key word'):
    set=ds[setname]
    s=mode+' '+setname+': "'+ a+'"'
    if 'add' ==mode:
        if a in set:s='"'+a+'" already in '+setname
        else:set.add(a)
    elif 'remove' ==mode:
        if a in set:set.remove(a)
        else:s='no "'+a+'" in'+setname
    print(1.0,s+'\n'+setname+' now :\n'+str(set)+'\n\n')
    print(set)
    
    
start(input('link:'))
print("command:\n\texit\n\tlist:\n\t(smt) add keyword")
while clt.running:
    a=input()
    if a=="exit":
        clt.exit()
        exit()
    elif a[:5]=="link:":
        start(a[5:])
    else:
        duty(a.split)


for i,j in maintranslator.items():
    print(i,':',j)
clt.exit()
print("live chat end")
input("press enter to exit")

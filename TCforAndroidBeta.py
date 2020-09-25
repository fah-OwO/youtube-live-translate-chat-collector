import time
# from time import time.sleep
import tkinter as tk
from pytchat import LiveChat
from threading import Thread as thr
from googletrans import Translator as gt
starttime=time.time()
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
        except: return f"{s}"  
        if tmp=='en':return f"{s}"          
        else:return f"{s}\n{en.text}" 
    z=s.lower()
    a=z.find('en')
    if a>0:
        if any(z.rfind(char1,0,a)!=-1 and z.find(char2,a)!=-1 for char1,char2 in zip('[(【','])】')) :
            return f"{s}" 
    if  any(word in s for word in keyword):
        return f"{s}"                       
    if n.isVerified:
        return t(s,n)
    if any(name ==n.name for name in member):
        return t(s,n)
    a=s.find(":")
    if a!=-1 and s.find(":",a+1)==-1:
        if len(s)-a<=3:return False
        if z[a:a+3]in (': 3',':ze'):return False
        if s[a+1] not in emoji:
            return f"{s}"                   
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
        self.livechat=False
        self.program_running=True
        self.running=False
        
        
    def setlink(self,link):
        if self.livechat:
            self.livechat.terminate()
        self.livechat = LiveChat(link)
        self.running=True

    def exit(self):
        self.livechat.terminate()
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
                            print(f"[ >{c.author.name} ({maintranslator[c.author.name]})]")
                            print(d,end="\n\n")
                        self.chatdata.tick()
                except KeyboardInterrupt:
                    self.livechat.terminate()
                    break
                except Exception as e:
                    print(e)
                    break
            time.sleep(0.1)
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
ds={'keyword':keyword,'member':member}
def duty(a,mode='add',setname='keyword'):
    # print(a,mode,setname,type(a))
    if type(a)==type(list()):
        if len (a)==1:a=a[0]
        elif len (a)==2:a,mode=a[:]
        elif len (a)==3:a,mode,setname=a[:]
        else:return
    set=ds[setname]
    s=mode+' '+setname+': "'+ a+'"'
    if 'add' ==mode:
        if a in set:s='"'+a+'" already in '+setname
        else:set.add(a)
    elif 'remove' ==mode:
        if a in set:set.remove(a)
        else:s='no "'+a+'" in'+setname
    print(1.0,s+'\n'+setname+' now :\n'+str(set)+'\n\n')
    
    
start(input('link:'))
print("command:\n\texit\n\tlink:\n\t(smt) add keyword")
while True:
    a=input()
    if a=="exit":
        break
    elif a[:5]=="link:":
        start(a[5:])
    elif a[:5]=="eval:":
        try :eval(a[5:])
        except Exception as e:print(e)
    elif len(a)<1:
        continue
    else:
        a=a.split()
        try:duty(a)
        except Exception as e:print(e)

# print("translator statistic")
print("time:",time.time()-starttime)
for i,j in maintranslator.items():
    print(i,':',j)
clt.exit()

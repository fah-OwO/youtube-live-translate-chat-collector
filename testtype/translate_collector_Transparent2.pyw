# if you dont want this window to be on top delete this line: "root.attributes("-topmost", True) "

# how to use :run this and put link on lowest tab and click ok
# (optional) you can add temporary keyword ore favorite translate by using middle tab and click add keyword/member button
# (can edit in code) there will be "sender:" tab which show sender and sending counting
# good luck and welcome to rabbit hole (kusa)
import time
import tkinter as tk
from pytchat import LiveChat
import threading
from googletrans import Translator as gt
starttime=time.time()
translator = gt()
keyword={'talking about'}
member=set()
emoji='[',']' ,'(' ,')' ,'<' ,'>','0','1','2','3','4','5','6','7','8','9'
transparentcolor="grey"
color=["aqua","black",transparentcolor]
end=tk.END
def condition(s,n):
    def t(s,n):
        tmp='en'                           
        try:
            en=translator.translate(s,dest="en")
            tmp=en.src
        except: return f" > {n.name}\n{s}"  
        if tmp=='en':return f" > {n.name}\n{s}"          
        else:return f" > {n.name}\n{s}\n{en.text}" 
    z=s.lower()
    a=z.find('en')
    if a>0:
        if any(z.rfind(char1,0,a)!=-1 and z.find(char2,a)!=-1 for char1,char2 in zip('[(【','])】')) :
            return s
    if  any(word in s for word in keyword):
        return s                     
    if n.isVerified:
        return t(s,n)
    if any(name ==n.name for name in member):
        return t(s,n)
    a=s.find(":")
    if a!=-1 and s.find(":",a+1)==-1:
        if len(s)-a<=3:return False
        elif z[a:a+3]in (': 3',':ze'):return False
        elif s[a+1] not in emoji:return s                   
    return False                                

maintranslator={}
def maintranslatoradd(st):
    if st in maintranslator:maintranslator[st]+=1
    else:maintranslator[st]=1
    
class collector(threading.Thread):
    def __init__(self,text):
        super(collector,self).__init__()
        self.livechat=False
        self.program_running=True
        self.running=False
        self.text=text
        
        
    def setlink(self,link):
        self.running=False
        if self.livechat:self.livechat.terminate()
        self.livechat = LiveChat(link)
        self.running=True
        t = threading.Thread(target=addtext, args=('collecting\n > '+ link,color,self.text))
        t.start()

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
                            t = threading.Thread(target=addtext, args=(d,color,self.text))
                            t.start()
                        self.chatdata.tick()
                except KeyboardInterrupt:
                    self.livechat.terminate()
                    break
            time.sleep(0.1)
    

def start(a,clt):
    try:
        clt.setlink(a)
    except Exception as e:
        print(e)

def addtext(sentence,color,text):
    text.insert(end,sentence+'\n\n')
    x=len(sentence)
    idx=text.search(sentence,'1.0',tk.END)
    pos = '{}+{}c'.format(idx, x)
    text.tag_add(color[0],idx,pos)
    for i in range(1,len(color)):
        time.sleep(20*(i-1)+1)
        if not text.winfo_exists():break
        idx=text.search(sentence,'1.0',tk.END)
        pos = '{}+{}c'.format(idx, x)
        text.tag_add(color[i],idx,pos)
    text.delete('1.0',pos)
ds={'keyword':keyword,'member':member}
def duty(a,mode='add',setname='keyword',text=False):
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
    if text:
        addtext(s+'\n'+setname+' now :\n'+str(set),color,text)
    else:
        print(s+'\n'+setname+' now :\n'+str(set)+'\n\n')
    
def command(root,text):
    while text.winfo_exists():
        a=input()
        if a=="exit":
            root.quit()
            break
        elif a[:5]=="link:":eval('start(a[5:])')#start(a[5:])
        elif a[:5]=="eval:":
            try :eval(a[5:])
            except Exception as e:print(e)
        elif len(a)<1:continue
        else:
            if "'" in a:
                x=a.find("'")+1
                y=a.find("'",x)
                if y+3>len(a):x=[a[x:y]]
                else:x=[a[x:y]]+a[y+1:].split()
            elif '"' in a:
                x=a.find('"')+1
                y=a.find('"',x)
                if y+3>len(a):x=[a[x:y]]
                else:x=[a[x:y]]+a[y+1:].split()
            else:
                x=a.split()
            print(x)
            try:duty(x,text=text)
            except Exception as e:print(e)
def main():
    root = tk.Tk()
    w, h = root.winfo_screenwidth(), root.winfo_screenheight()
    root.wm_attributes('-fullscreen','true')
    root.attributes("-topmost", True)
    root.wait_visibility(root)
    root.attributes("-transparentcolor", transparentcolor)
    text = tk.Text(root,height=h,width=w,font="Sans 24",background=transparentcolor,foreground="white",padx=30,pady=30)
    for i in color[:-1]:
        text.tag_config(i, background=i)
    text.tag_config(color[-1], background=color[-1],foreground=color[-1])
    text.pack()

    clt=collector(text)
    clt.start()
    start(input('link:'),clt)
    print("command:\n\t(smt) add keyword")
    commandthread=threading.Thread(target=command,args=(root,text))
    commandthread.start()
    root.mainloop()
    clt.exit()
    print("time:",time.time()-starttime)
    for i,j in maintranslator.items():
        print(i,':',j)
    input("press enter to exit")
if __name__ == "__main__":
    main()

import time
import tkinter as tk
from pytchat import LiveChat
import threading
from googletrans import Translator as gt
tmp=input('link:')
starttime=time.time()
translator = gt()
keyword={'talking about'}
member=set()
blockmember=set()
blockkeyword={'[ES]'}
autoclassfier = True
waittime=[0,1,20]
ds={'auto':autoclassfier,
    'waittime':waittime,
    'keyword':keyword,
    'member':member,
    'blockkeyword':blockkeyword,
    'blockmember':blockmember}
emoji='[',']' ,'(' ,')' ,'<' ,'>','0','1','2','3','4','5','6','7','8','9'
transparentcolor="grey"
color=["aqua","black",transparentcolor]
end=tk.END
def tab_control(a):return a+' '*(20-len(a))+':\t'

def func(list1,list2):
    a=time.monotonic_ns() 
    color,text=list1
    sentence,turn,l,lnow=list2
    s=sentence.split('\n')
    sum=sentence.count('\n')
    rt=0
    if  turn ==len(color)-1:
        idx=str (lnow-l)
        pos=float(sentence.count('\n'))
        text.delete(idx,tk.END)
        return rt
    else:
        for i in s:
            idx=str (lnow-l+sum)
            if turn==0:
                idx='1.0'
                text.insert(idx,i+'\n')
                rt+=1
            else:sum-=1
            pos= '{}+{}c'.format(idx, len(i))
            text.tag_add(color[turn],idx,pos)
        return rt

class addtext(threading.Thread):
    def __init__(self,func,args,wait=[0,2,7]):
        super(addtext,self).__init__()
        self.program_running=True
        self.running=False
        self.func,self.args,self.wait=func,args,wait
        self.list=[]
        for i in range(len(self.wait)):
            self.list.append(list())
        self.time=int(time.time())
        self.l=1.0
    def settext(self,sentence):
        sentence='\n'.join([i for i in sentence.split('\n')[::-1]])
        sentencecont=sentence.count('\n')
        # self.l+=self.func(self.args,[sentence,0,0]+[self.l])
        for i in range(len(self.wait)):
            self.list[i].append([int(time.time()+self.wait[i]),sentence,i,self.l+sentencecont])
        self.running=True

    def exit(self):
        self.running=False
        self.program_running=False

    def run(self):
        while self.program_running:
                for i in range(len(self.list)):
                    while self.list[i] and self.list[i][0][0]<=time.time() and self.running:
                        a=self.list[i][0]
                        self.l+=self.func(self.args,a[1:]+[self.l])#self.l-=
                        self.list[i].pop(0)
                time.sleep(0.1)
def condition(s,n):
    if any(word in s for word in blockkeyword) or n.name in blockmember:
        return False
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
    if any(name ==n.name for name in member):
        return t(s,n)
    if bool(ds['auto']) :                     
        if n.isVerified:
            return t(s,n)
        a=s.find(":")
        if a>0 and s.find(":",a+1)==-1:
            if len(s)-a<=3:return False
            elif z[a:a+3]in (': 3',':ze'):return False
            elif s[a+1] not in emoji:return s                   
    return False                                

maintranslator={}
def maintranslatoradd(st):
    if st in maintranslator:maintranslator[st]+=1
    else:maintranslator[st]=1
    
class collector(threading.Thread):
    def __init__(self,text,textor):
        super(collector,self).__init__()
        self.livechat=False
        self.program_running=True
        self.running=False
        self.text=textor
        
        
    def setlink(self,link):
        self.running=False
        if self.livechat:self.livechat.terminate()
        self.livechat = LiveChat(link)
        self.running=True
        self.text.settext('collecting\n > '+ link+'\n\n')

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
                            self.text.settext(d+'\n\n')
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
        s+='\n'+setname+' now :\n'+str(set)
    elif 'remove' ==mode:
        if a in set:set.remove(a)
        else:s='no "'+a+'" in'+setname
        s+='\n'+setname+' now :\n'+str(set)
    else:s="error mode\n"
    if text:
        text.settext(s+'\n\n')
    else:
        print(s+'\n\n')
    

    
def main():
    root = tk.Tk()
    w, h = root.winfo_screenwidth(), root.winfo_screenheight()
    root.wm_attributes('-fullscreen','true')
    root.attributes("-topmost", True)
    root.wait_visibility(root)
    root.attributes("-transparentcolor", transparentcolor)
    root.attributes("-alpha",0.8)
    text = tk.Text(root,height=h,width=w,font="Sans 24",background=transparentcolor,foreground="white",padx=30,pady=30)
    for i in color[:-1]:
        text.tag_config(i, background=i)
    text.tag_config(color[-1], background=color[-1],foreground=color[-1])
    text.pack()

    textor=addtext(func,(color,text),waittime)
    clt=collector(text,textor)
    # cmd=command(root,clt,textor)
    textor.start()
    clt.start()
    # cmd.start()
    start(tmp,clt)
    print('command:')
    print("\tlink:(new link)")
    print("\ttoggle auto")
    print("\tprint all")
    print("\tset waittime (value)")
    print("\tsmt\t|add\t|keyword")
    print("\t'smt'\t|remove\t|member")
    print("\t\"smt\"\t|\t|blockkeyword")
    print("\t\t|\t|blockmember")
    def command():
        a=input()
        if a=='':pass
        elif a=="exit":
            clt.exit()
            textor.exit()
            root.quit()
            return
            # clt.exit()
            # textor.exit()
            # root.quit()
            # exit()
        elif 'youtube.com' in a:clt.setlink(a[a.find('youtube.com'):])
        elif a[:5]=="link:":clt.setlink(a[5:])
        elif 'toggle' in a:
            a=a.split()[1]
            if a in ds:ds[a]=not ds[a]
            else: print(a,'not in ',ds)
            print(tab_control(a+' now '),ds[a])
        elif a[:5]=='print':
            if "all" in a[6:]:
                print('\n'.join([tab_control(x)+str(y) for x,y in ds.items()]))# print('\n'.join([x+' '*(20-len(x))+':\t'+str(y) for x,y in ds.items()]))
        elif 'set' in a[:5]:
            a=a.split()
            if len(a)>3:print('error')
            elif a[1] in ds:
                if type(ds[a[1]])==type([]):ds[a[1]][-1]=type(ds[a[1]][-1])(a[2])
                else:ds[a[1]]=type(ds[a[1]])(a[2])
            else: print(a[1],'not in',ds)
            print(ds[a[1]])
        elif a[:5]=="eval:":
            try :eval(a[5:])
            except Exception as e:print(e)
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
            try:duty(x,text=textor)
            except Exception as e:print(e)
        root.after(500, command)
    root.after(500, command)
    root.mainloop()
    print("time:",time.time()-starttime)
    for i,j in maintranslator.items():
        print(tab_control(i),j)
    clt.exit()
    textor.exit()
    input("press enter to exit")
if __name__ == "__main__":
    try:main()
    except Exception as e:
        print(e)

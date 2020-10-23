import time
import tkinter as tk
from pytchat import LiveChat
import threading
from googletrans import Translator as gt

startline=1.0
startline=float(startline)
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
def tab_control(a,char=20):return a+' '*(char-len(a))+':\t'

#tkinter line controller
def clear(text,textor):
    textor.stoprunning()
    for i in ds:
        if any(a in i for a in['word','member']):
            print(i+' clear')
            ds[i]=[]

    textor.clear()
    text.delete('1.0',tk.END)
    text.insert('1.0','\n'*int(20))
    textor.startrunning()
def func(list1,list2):
    a=time.monotonic_ns() 
    color,text=list1
    sentence,turn,l,lnow=list2
    s=sentence.split('\n')
    sum=sentence.count('\n')
    rt=0
    
    for i in s:
        idx=str (lnow-l+sum+20)
        if turn==0:
            idx='21.0'#startline
            text.insert(idx,i+'\n')
            rt+=1
        else:sum-=1
        pos= '{}+{}c'.format(idx, len(i))
        text.tag_add('center',idx,pos)
        text.tag_add(color[turn],idx+'+1c',pos)
    return rt

class addtext(threading.Thread):
    def __init__(self,func,args,wait=[0,2,7]):
        super(addtext,self).__init__()
        self.program_running=True
        self.running=False
        self.func,self.args,self.wait=func,args,wait
        self.list=[]
        for i in range(len(self.wait)):self.list.append(list())
        # self.time=int(time.time())
        self.l=21.0
    def settext(self,sentence):
        sentence='\n'.join([' '+i if len(i)<100 else '\n'.join([' '+i[j:j+100] for j in range(0,len(i),100)][::-1]) for i in sentence.split('\n')[::-1]])
        sentencecont=sentence.count('\n')
        for i in range(len(self.wait)):self.list[i].append([int(time.time()+self.wait[i]),sentence,i,self.l+sentencecont])
        self.running=True

    def exit(self):
        self.running=False
        self.program_running=False
        
    def stoprunning(self):self.running=False
    def clear(self):
        self.list=[]
        for i in range(len(self.wait)):self.list.append(list())
    def startrunning(self):self.running=True

    def run(self):
        while self.program_running:
                for i in range(len(self.list)):
                    while self.list[i] and self.list[i][0][0]<=time.time() and self.running:
                        a=self.list[i][0]
                        self.l+=self.func(self.args,a[1:]+[self.l])
                        self.list[i].pop(0)
                time.sleep(0.1)

# condition
def condition(s,n):
    if any(word in s for word in blockkeyword) or n.name in blockmember:return False
    def t(s,n):
        tmp='en'                           
        try:
            en=translator.translate(s,dest="en")
            tmp=en.src
        except: return " > "+n.name+"\n"+s  
        if tmp=='en':return " > "+n.name+"\n"+s          
        else:return " > "+n.name+"\n"+s+"\n"+en.text
    z=s.lower()
    a=z.find('en')
    if a>0:
        if any(z.rfind(char1,0,a)!=-1 and z.find(char2,a)!=-1 for char1,char2 in zip('[(【','])】')) :
            return s
    elif  any(word in s for word in keyword):
        return s
    elif any(name ==n.name for name in member):
        return t(s,n)
    elif bool(ds['auto']) :                     
        if n.isVerified:
            return t(s,n)
        a=s.find(":")
        if a>0 and s.find(":",a+1)==-1:
            if len(s)-a<=3:return False
            elif z[a:a+3]in (': 3',':ze'):return False
            elif s[a+1] not in emoji:return s                   
    return False                                
# collect translator name
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
        try:
            self.livechat = LiveChat(link)
            self.running=True
            self.text.settext('collecting\n > '+ link+'\n')
            return True
        except:
            print("link error")
            self.running=False
            return False

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
                            self.text.settext(d+'\n')
                        self.chatdata.tick()
                except KeyboardInterrupt:
                    self.livechat.terminate()
                    break
            time.sleep(0.1)
    
# keyword/member
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
    if text:text.settext(s+'\n')
    else:print(s+'\n')
    

def main():
    tmp=input('link:')
    root = tk.Tk()
    w, h = root.winfo_screenwidth(), root.winfo_screenheight()
    root.wm_attributes('-fullscreen','true')
    root.attributes("-topmost", True)
    root.wait_visibility(root)
    root.attributes("-transparentcolor", transparentcolor)
    root.attributes("-alpha",0.8)
    text = tk.Text(root,height=h,width=w,font="Sans 24",background=transparentcolor,foreground="white",padx=30,pady=30)
    for i in color[:-1]:text.tag_config(i, background=i)
    text.tag_config(color[-1], background=color[-1],foreground=color[-1])
    text.tag_configure("center", justify='center')
    text.pack()
    text.insert('1.0','\n'*int(20))
    textor=addtext(func,(color,text),waittime)
    clt=collector(text,textor)
    textor.start()
    clt.start()
    while not clt.setlink(tmp):
        tmp=input('link:')
    def printcommand():
        print('command:')
        print("\tlink:(new link)")
        print("\tset waittime (value)")
        print("\ttoggle auto")
        print("\tprint all")
        print("\tsmt\t|add\t|keyword")
        print("\t'smt'\t|remove\t|member")
        print("\t\"smt\"\t|\t|blockkeyword")
        print("\t\t|\t|blockmember")
    printcommand()
    def command():
        a=input()
        if a=='' or a=='?':printcommand()
        elif a=="clear":clear(text,textor)
        elif a=="exit":clt.exit();textor.exit();root.quit();return
        elif 'youtube.com' in a:clt.setlink(a[a.find('youtube.com'):])
        elif a[:5]=="link:":clt.setlink(a[5:])
        elif 'toggle' in a:
            a=a.split()[1]
            if a in ds:ds[a]=not ds[a]
            else: print(a,'not in ',ds)
            print(tab_control(a+' now '),ds[a])
        elif a[:5]=='print':
            if "all" in a[6:]:print('\n'.join([tab_control(x)+str(y) for x,y in ds.items()]))
            else:
                try:print(eval(a[5:]))
                except Exception as e:print(e)
        elif 'set' in a[:5]:
            a=a.split()
            try:
                if len(a)>3:print('error')
                elif a[1] in ds and type(ds[a[1]])==type([]):ds[a[1]][-1]=type(ds[a[1]][-1])(a[2])
                else:eval(a[1]+'=type('+a[1]+')('+a[2]+')')
                print(ds[a[1]])
            except Exception as e:print('Error'+e+'\n or '+a[1]+' not in '+ds)
        elif a[:5]=="eval:":
            try :eval(a[5:])
            except Exception as e:print(e)
        else:
            for i in ["'",'"']:
                if i in a:
                    x=a.find(i)+1
                    y=a.find(i,x)
                    if y+3>len(a):x=[a[x:y]]
                    else:x=[a[x:y]]+a[y+1:].split()
                    break
            else:x=a.split()
            print(x)
            try:duty(x,text=textor)
            except Exception as e:print(e)
        root.after(500, command)
    root.after(500, command)
    try:root.mainloop()
    except:root.quit()
    print("time:",time.time()-starttime)
    for x,y in sorted([(i,j) for j,i in maintranslator.items()]):print(tab_control(y),x)
    clt.exit()
    textor.exit()
    time.sleep(30)
    return
if __name__ == "__main__":
    main()

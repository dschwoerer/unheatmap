#!/usr/bin/python3

import sys
from PIL import Image
from PIL import ImageTk as itk
import tkinter as tk

class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self,master)
        self.grid();
        self.createWidgets()

    def createWidgets(self):
        self.menu    = tk.Frame(self)
        self.menu.grid()
        self.menu.info = tk.Label(self.menu,
                        text='Click on one end of the scale',
                        width=40)
        self.menu.info.pack(side='left')
        self.menu.scale=[]
        for i in [0,1]:
            self.menu.scale.append(Menu1(self.menu,
                        lambda index=i:self.__setScale(index)))
            self.menu.scale[i].value.set("%d.00"%100**(1-i))
        self.menu.log=tk.StringVar()
        self.menu.log.set('Lin')
        self.menu.logWx=tk.Button(self.menu
                        ,textvariable=self.menu.log,
                        command=self.__toggleLog)
        self.menu.logWx.pack(side='left')
        self.menu.out = Menu1(self.menu,
                    cmd=lambda index=2 :self.__setScale(index))
        self.im=itk.PhotoImage(im)
        self.image      = tk.Canvas(self,height=self.im.height(),
                                    width=self.im.width())
        self.image.create_image(0,0,image=self.im,anchor=tk.NW)
        self.image.grid()
        self.image.bind('<Button-1>',self.__clicked)
        self.bind_all('<Up>'    ,self.__up)
        self.bind_all('<Down>'  ,self.__down)
        self.bind_all('<Right>' ,self.__right)
        self.bind_all('<Left>'  ,self.__left)
        self.bind_all('<Return>',self.__redraw)
        self.scale=[];
        self.mode=-1
        self.pixels=im.load()
        
    def resetScale(self):
        self.scale=[]
        self.mode=-1
    def __setScale(self,index):
        self.mode=index-1
    def __clicked(self,event):
        if self.mode < 2:
            self.mode+=1
        if (self.mode < 2):
            if self.mode < len(self.scale):
                self.scale[self.mode]=(event.x,event.y)
            else:
                self.scale.append((event.x,event.y))
            self.__redraw()
            if len(self.scale)==2:
                self.__calcColorScale()
        else:
            self.analyze=(event.x,event.y)
            self.__analyze()
            self.__redraw()
            ty=int(event.type)
            if ty == 4:
                self.image.bind('<Motion>',self.__clicked)
                self.bind_all('<ButtonRelease-1>',self.__unclick)
    
    def __unclick(self,event):
        self.image.unbind('<Motion>')
        

    def __move(self,event,vec):
        if (self.mode < 2):
            newpos=myadd(self.scale[self.mode],vec)
            self.scale[self.mode]=newpos
            if self.mode==1:
                self.__calcColorScale()
        elif self.mode==2:
            newpos=myadd(self.analyze,vec)
            self.analyze=newpos
            self.__analyze()
        else:
            print(self.mode)
        self.__redraw()
        
    def __up(self,event):
        self.__move(event,( 0,-1))
    def __down(self,event):
        self.__move(event,( 0, 1))
    def __right(self,event):
        self.__move(event,( 1, 0))
    def __left(self,event):
        self.__move(event,(-1, 0))

    def __toggleLog(self,event=None):
        if conf.log:
            conf.log=False
            self.menu.log.set('Lin')
        else:
            conf.log=True
            self.menu.log.set('Log')
    def __calcColorScale(self):
        dx=self.scale[0][0]-self.scale[1][0]
        dy=self.scale[0][1]-self.scale[1][1]
        #print(self.scale,dx,dy)
        if abs(dx)>abs(dy):
            diff=abs(dx)
            direc=[sign(dx),0]
        else:
            diff=abs(dy)
            direc=[0,sign(dy)]
        #print(diff,direc)
        self.colors=[]
        pos=list(self.scale[1])
        #print(type(pos))
        for i in range(diff+1):
            self.colors.append(self.pixels[tuple(pos)])
            pos=myadd(pos,direc)
            #print(pos)
        mmax=0
        for i in range(len(self.colors)-1):
            cm=calcdiff(self.colors[i],self.colors[i+1])
            if cm>mmax:
                mmax=cm
        self.colors_maxdiff=mmax
    def __analyze(self):
        x=self.analyze[0]
        y=self.analyze[1]
        if x < 0 or y < 0 or x >= self.im.width() or y >= self.im.height() :
            out='N/A'
            self.menu.out.value.set(out)
            return out
        col=self.pixels[self.analyze]
        cdiff=1000
        idiff=-1
        for i in range(len(self.colors)):
            ccdiff=calcdiff(col,self.colors[i])
            if ccdiff < cdiff:
                cdiff=ccdiff
                idiff=i
        if cdiff < self.colors_maxdiff:
            out=idiff/len(self.colors)
            low  =float(self.menu.scale[0].value.get())
            upper=float(self.menu.scale[1].value.get())
            try:
                if conf.log:
                    if low <= 0:
                        raise Exception("Invalid input - Value %f needs to be larger > 0 for log scale"%low)
                    if upper <= 0:
                        raise Exception("Invalid input - Value %f needs to be larger > 0 for log scale"%upper)
                    #out=upper*(low/upper)**out
                    out=upper*(low/upper)**out
                else:
                    out=low+out*(upper-low)
            except e:
                print(e)
                out=low+out*(upper-low)
                pass
            if conf.stdout:
                print(out)
        else:
            if conf.stdout:
                print("Could not find color in scale!")
                print(cdiff,len(self.colors))
            out='N/A'
        self.menu.out.value.set(out)
        
    def __redraw(self,event=None):
        self.image.create_image(0,0,image=self.im,anchor=tk.NW)
        #print(self.mode)
        for i in range(len(self.scale)):
            drawCross(self.image,self.scale[i])
            drawArrow(self.image,self.scale[i],
                    (self.menu.winfo_x()+
                     self.menu.scale[i].valueWx.winfo_x()+
                     self.menu.scale[i].valueWx.winfo_width()/2,0))
        if self.mode == 2:
            drawCross(self.image,self.analyze)


class Menu1():
    def __init__(self,master,cmd):
        
        self.Set = tk.Button(master,text='Set',
                             command=cmd)
        self.Set.pack(side='left')
        self.value = tk.StringVar()
        self.value.set('100.00')
        self.isFloat = master.register(self.__isFloat)
        self.valueWx = tk.Entry(master,
            width=8, textvariable=self.value,
            validate='key',
            validatecommand = (self.isFloat,'%P'))
        self.valueWx.pack(side='left')
    def __isFloat(self,text):
        try:
            float(text)
            return True
        except:
            return False
class Config():
    stdout=False
    log=False
conf=Config()
try:
    im=Image.open(sys.argv[1])
except:
    print("Usage:")
    print("\t%s <path-to-image>"%sys.argv[0])
    sys.exit(1)

def calcdiff(c1,c2):
    diff=0;
    for i in range(3):
        diff+=abs(c1[i]-c2[i])
    return diff

def sign(i):
    if i > 0:
        return 1
    if i < 0:
        return -1
    return 0

def myadd(l1,l2):
    ret=[]
    for i in range(len(l1)):
        ret.append(l1[i]+l2[i])
    return ret

def drawCross(canvas,p,size=2):
    x=p[0]
    y=p[1]
    canvas.create_line(x-size,y,x+size,y)
    canvas.create_line(x,y-size,x,y+size)
def drawArrow(canvas, p1,p2):
    canvas.create_line(p1[0],p1[1],p2[0],p2[1])

root = tk.Tk()
app = Application()
app.master.title('Un-Heat-Map')
app.mainloop()

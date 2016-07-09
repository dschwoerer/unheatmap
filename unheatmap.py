#!/usr/bin/python3

import os
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
        self.quitButton = tk.Button(self,text='Quit',
                                    command=self.quit)
        self.quitButton.grid()
        self.scale0     = tk.Button(self,text='FindScale',
                                    command=self.resetScale)
        self.scale0.grid()
        self.im=itk.PhotoImage(im)
        self.image      = tk.Canvas(self,height=self.im.height(),width=self.im.width())
        self.image.create_image(0,0,image=self.im,anchor=tk.NW)
        self.image.grid()
        self.image.bind('<Button-1>',self.__clicked)
        self.bind_all('<Up>',self.__up)
        self.bind_all('<Down>',self.__down)
        self.bind_all('<Return>',self.__redraw)
        self.scale=[];
        self.mode=-1
        self.pixels=im.load()
    def resetScale(self):
        self.scale=[]
        self.mode=-1
    def __clicked(self,event):
        if self.mode < 2:
            self.mode+=1
        #print(self.mode)
        if (self.mode < 2):
            if self.mode < len(self.scale):
                self.scale[self.mode]=(event.x,event.y)
            else:
                self.scale.append((event.x,event.y))
            drawCross(self.image,(event.x,event.y))
            #self.__redraw()
            if len(self.scale)==2:
                self.__calcColorScale()
                #print(self.colors)
        else:
            #print('I should analyze this point')
            drawCross(self.image,(event.x,event.y))
            self.analyze=(event.x,event.y)
            self.__analyze()
    def up(self,event):
        print('fu)')

    def __up(self,event):
        if (self.mode < 2):
            newpos=(self.scale[self.mode][0],self.scale[self.mode][1]-1)
            self.scale[self.mode]=newpos
            if self.mode==1:
                self.__calcColorScale()
        elif self.mode==2:
            newpos=(self.analyze[0],self.analyze[1]-1)
            self.analyze=newpos
            self.__analyze()
        else:
            print(self.mode)
        #drawCross(self.image,newpos)
        self.__redraw()
    def __down(self,event):
        if (self.mode < 2):
            newpos=(self.scale[self.mode][0],self.scale[self.mode][1]+1)
            self.scale[self.mode]=newpos
            if self.mode==1:
                self.__calcColorScale()
        elif self.mode==2:
            newpos=(self.analyze[0],self.analyze[1]+1)
            self.analyze=newpos
            self.__analyze()
        #drawCross(self.image,newpos)
        self.__redraw()
            
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
        col=self.pixels[self.analyze]
        cdiff=1000
        idiff=-1
        for i in range(len(self.colors)):
            ccdiff=calcdiff(col,self.colors[i])
            if ccdiff < cdiff:
                cdiff=ccdiff
                idiff=i
        if cdiff < self.colors_maxdiff:
            print(idiff/len(self.colors))
            #print(col,self.colors[idiff])
        else:
            print("Could not find color in scale!")
            print(cdiff,len(self.colors))
    def __redraw(self,event):
        self.__redraw();
    def __redraw(self):
        self.image.create_image(0,0,image=self.im,anchor=tk.NW)
        #print(self.mode)
        for i in range(self.mode+1):
            if i < 2:
                drawCross(self.image,self.scale[i])
            elif i == 2:
                drawCross(self.image,self.analyze)
        
im=Image.open(sys.argv[1])

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
    for i in range(len(l1)):
        l1[i]+=l2[i]
    return l1

def drawCross(canvas,p,size=2):
    x=p[0]
    y=p[1]
    canvas.create_line(x-size,y,x+size,y)
    canvas.create_line(x,y-size,x,y+size)

root = tk.Tk()
app = Application()
app.master.title('Un-Heat-Map')
app.mainloop()

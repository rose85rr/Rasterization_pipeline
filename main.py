# -*- coding: utf-8 -*-
"""
Created on Tue Mar  9 19:01:09 2021

@author: monok
"""

import math
import numpy as np
from tkinter import *
from PIL import ImageTk, Image
import os
import matplotlib
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D
from sklearn.preprocessing import normalize

class Window():
    def __init__(self, main):
        Label(root,text='VIEW：').grid(row=2,column=0)
        #self.scaleEntry=Entry(root)
        #self.scaleEntry.grid(row=2,column=1)
        #self.scaleEntry.insert(0,'2')
        Button(root,text='View Coordinates',command=self.viewCoordinates).grid(row=2,column=1,columnspan=1)
        Label(root,text='CLIP：').grid(row=3,column=0)
        Button(root,text='Clip Coordinates',command=self.clipCoordinates).grid(row=3,column=1,columnspan=1)
        Label(root,text='NORMALIZED：').grid(row=4,column=0)
        Button(root,text='Normalized Coordinates',command=self.normalizedCoordinates).grid(row=4,column=1,columnspan=1)
        Label(root,text='IMAGE：').grid(row=5,column=0)
        Button(root,text='Image Coordinates',command=self.imageCoordinates).grid(row=5,column=1,columnspan=1)
        self.vertice = np.array([[0.0, 0, 3, 2], [2, 2, 0, 0], [2, -2, 0, 0], 
        [-2, -2, 0, 0], [-2, 2, 0, 0]]) 
        self.camera = [2,3,5]
        self.cube = 3
        self.after = np.array([[0.0,0.0],[0,0],[0,0],[0,0],[0,0]])
        self.labels = ['-1','0','1']
        self.drawPic()
    def move_camera(self):
        i = 0
        for p in self.vertice:
            self.vertice[i][0] = p[0] - self.camera[0]
            self.vertice[i][1] = p[1] - self.camera[1]
            self.vertice[i][2] = p[2] - self.camera[2]
            self.vertice[i][3] = p[3] - self.camera[2]
            i = i+1
        y = [0,1,0]
        w = [self.vertice[0][0],self.vertice[0][1],self.vertice[0][2]]
        y = np.matrix(y)
        w = np.matrix(w)
        u = np.cross(y,w)
        v = np.cross(w,u)
        u = np.matrix(normalize(u, axis=1, norm='l1'))
        v = np.matrix(normalize(v, axis=1, norm='l1'))
        r = np.vstack((u,v,w))
        invr = np.linalg.inv(r)
        #print( "r = ", r,"\nr-1 = ", invr,"\nr*r = ", np.dot(r, invr),"\nr*r = ",np.dot(invr, r))
        i = 0
        temp = []
        for p in self.vertice:
            for q in range(3):
                temp.append(self.vertice[i][q])
            i = i+1
        temp = np.matrix(temp)
        temp.resize((5,3))
        newplace = np.dot(temp, invr)
        newplace = np.array(newplace)
        i = 0
        for p in self.vertice:
            print(newplace[i])
            self.vertice[i][0] = newplace[i][0]
            self.vertice[i][1] = newplace[i][1]
            self.vertice[i][2] = newplace[i][2]
            self.vertice[i][3] = newplace[i][2]
            i = i+1
        self.vertice = np.matrix(self.vertice)
        print("ver:",self.vertice)
        self.camera[0] = 0
        self.camera[1] = 0
        self.camera[2] = 0
    def viewCoordinates(self):
        self.move_camera()
        print("camera now:", self.camera)
        self.drawPic()
        self.test3d()
    def clipCoordinates(self):
        l,r,b,t,n,f = 0-self.cube,self.cube,0-self.cube,self.cube,self.cube,0-self.cube
        a = np.matrix([[2/(r-l), 0, 0, (l+r)/(l-r)],[0, 2/(t-b), 0, (b+t)/(b-t)],
                      [0, 0, 2/(n-f), (f+n)/(f-n)], [0, 0, 0, 1]])
        self.vertice = (np.dot(a,self.vertice.T)).T
        print(self.vertice)
        self.drawPic()
        self.test3d()
    def normalizedCoordinates(self):
        l,r,b,t,n,f = 0-self.cube,self.cube,0-self.cube,self.cube,self.cube,0-self.cube
        full_a = np.matrix([[(2*n)/(r-l), 0, (r+l)/(r-l), 0],[0, (2*n)/(t-b), 0, (t+b)/(t-b)],
                      [0, 0, -1*(f+n)/(f-n), (-2*f*n)/(f-n)], [0, 0, -1, 0]])
        self.vertice = (np.dot(full_a,self.vertice.T)).T
        print(self.vertice)
        self.drawPic()
        self.test3d()
    def imageCoordinates(self):
        temp = np.array(self.vertice)
        i = 0
        for p in temp:
            self.after[i][0] = p[0]
            self.after[i][1] = p[1]
            i = i+1
        self.drawPic()
        self.test3d()
    def test3d(self):
        temp = np.array(self.vertice)
        ver = 8
        vec_x = []
        vec_y = []
        vec_z = []
        for p in temp:
            vec_x.append(p[0])
            vec_y.append(p[1])
            vec_z.append(p[2])
        vecStart_x = [vec_x[0],vec_x[0],vec_x[0],vec_x[0],vec_x[1],vec_x[2],vec_x[3],vec_x[4]]
        vecStart_y = [vec_y[0],vec_y[0],vec_y[0],vec_y[0],vec_y[1],vec_y[2],vec_y[3],vec_y[4]]
        vecStart_z = [vec_z[0],vec_z[0],vec_z[0],vec_z[0],vec_z[1],vec_z[2],vec_z[3],vec_z[4]]
        vecEnd_x = [vec_x[1],vec_x[2],vec_x[3],vec_x[4],vec_x[2],vec_x[3],vec_x[4],vec_x[1]]
        vecEnd_y = [vec_y[1],vec_y[2],vec_y[3],vec_y[4],vec_y[2],vec_y[3],vec_y[4],vec_y[1]]
        vecEnd_z  =[vec_z[1],vec_z[2],vec_z[3],vec_z[4],vec_z[2],vec_z[3],vec_z[4],vec_z[1]]
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(self.camera[0], self.camera[1], self.camera[2], cmap='Blues', marker='o', label='My Points 2')
        
        for i in range(ver):
            ax.plot([vecStart_x[i], vecEnd_x[i]], [vecStart_y[i],vecEnd_y[i]],zs=[vecStart_z[i],vecEnd_z[i]])
        plt.savefig('hw4_2.png')
        self.img = ImageTk.PhotoImage(Image.open("hw4_2.png"))
        self.chart = Label(root, image = self.img)
        self.chart.image = self.img
        self.chart.grid(row=0,column=2)
        self.chart.configure(image = self.img)

    def drawPic(self): 
        vx = [self.after[0][0],self.after[1][0],self.after[2][0],self.after[3][0],self.after[4][0]]
        vy = [self.after[0][1],self.after[1][1],self.after[2][1],self.after[3][1],self.after[4][1]]
        
        #AB AC AD AE
        line1x = [vx[0],vx[1]]
        line1y = [vy[0],vy[1]]
        line2x = [vx[0],vx[2]]
        line2y = [vy[0],vy[2]]
        line3x = [vx[0],vx[3]]
        line3y = [vy[0],vy[3]] 
        line4x = [vx[0],vx[4]]
        line4y = [vy[0],vy[4]]
        
        line5x = [vx[1],vx[2]]
        line5y = [vy[1],vy[2]]
        line6x = [vx[2],vx[3]]
        line6y = [vy[2],vy[3]]
        line7x = [vx[3],vx[4]]
        line7y = [vy[3],vy[4]]
        line8x = [vx[4],vx[1]]
        line8y = [vy[4],vy[1]]

        #繪製在同一個figure中
        plt.figure()
        
        #x y = 0的黑線
        plt.axhline(0, color='black')
        plt.axvline(0, color='black')

       
        plt.plot(line1x,line1y,line2x,line2y,line3x,line3y,line4x,line4y, marker = ',')
        plt.plot(line5x,line5y,line6x,line6y,line7x,line7y,line8x,line8y, marker = ',')
        #擷取x,y的某一部分
        plt.xlim((-1,1))
        plt.ylim((-1,1))
        #正方形
        plt.gca().set_aspect('equal', adjustable='box')
        #設定x,y的座標描述標籤
        plt.xlabel("X")
        plt.ylabel("Y")
        #設定x刻度的間隔
        new_ticks = np.linspace(-3,3,3)
        new_ticks2 = np.linspace(-3,3,3)
        plt.xticks(new_ticks)
        plt.yticks(new_ticks2)
        #plt.yticks(new_ticks2, self.labels)
        #plt.yticks([-2, -1.5, 0, 1.5, 3],
                   #[r'$Really\ bad\ \alpha$', r'$bad$', r'$normal$', r'$good$', r'$very\ good$'])#r表示正則化,$$表示用數學字型輸出
        #網格線
        plt.grid(True,linestyle = "--",color = 'gray' ,linewidth = '0.5',axis='both')
        plt.savefig('hw4.png')
        self.img = ImageTk.PhotoImage(Image.open("hw4.png"))
        self.chart = Label(root, image = self.img)
        self.chart.image = self.img
        self.chart.grid(row=0,column=1)
        self.chart.configure(image = self.img)


if __name__ == '__main__':    
    root = Tk() 
    Window(root)
    root.title('HW4')
    root.geometry("1000x600+100+100")
    #在Tk的GUI上放置一個畫布，並用.grid()來調整佈局

    #放置標籤、文字框和按鈕等部件，並設定文字框的預設值和按鈕的事件函式
    
    
        #啟動事件迴圈
    root.mainloop()
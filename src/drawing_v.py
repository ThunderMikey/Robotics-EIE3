#!/usr/bin/env python
import time
import random
import math
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cm as cm



def calcX():
    return random.gauss(80,3) + 70*(math.sin(t)) # in cm
def calcY():
    return random.gauss(70,3) + 60*(math.sin(2*t)) # in cm
def calcW():
    return random.random()
def calcTheta():
    return random.randint(0,360)

class Canvas:
    def __init__(self,map_size=210, virtual=False):
        self.map_size    = map_size    # in cm
        self.canvas_size = 768         # in pixels
        self.margin      = 0.05*map_size
        self.scale       = self.canvas_size/(map_size+2*self.margin)
        self.virtual = virtual
        x = np.arange(10)
        ys = [i+x+(i*x)**2 for i in range(20)]
        self.colors = cm.rainbow(np.linspace(0, 1, len(ys)))
        self.counter = 0

    def drawLine(self,line):
        x1 = self.__screenX(line[0])
        y1 = self.__screenY(line[1])
        x2 = self.__screenX(line[2])
        y2 = self.__screenY(line[3])
        if self.virtual:
            plt.figure(num=1,figsize=(30,30))
            plt.plot([x1,x2],[y1,y2])
        print "drawLine:" + str((x1,y1,x2,y2))

    def drawParticles(self,data):
        display = [(self.__screenX(d[0][0])+d[1],self.__screenY(d[0][1])+d[1]) for d in data]
        if self.virtual:
            plt.ion()
            plt.figure(num=1,figsize=(10,10))
            plt.plot([i[0] for i in display],[i[1] for i in display],"ro",c=self.colors[self.counter])
            plt.pause(0.05)
            self.counter+=1
        else:
            print "drawParticles:" + str(display)
    def __screenX(self,x):
        return (x + self.margin)*self.scale
    def __screenY(self,y):
        return (self.map_size + self.margin - y)*self.scale

class Map:
    def __init__(self, canvas):
        self.walls = [];
        self.canvas = canvas
        self.virtual = False
        if canvas.virtual:
            self.virtual = True
    def add_wall(self,wall):
        self.walls.append(wall)
    def clear(self):
        self.walls = []
    def draw(self):
        for wall in self.walls:
            self.canvas.drawLine(wall)
        if self.virtual:
            plt.show(block=False)

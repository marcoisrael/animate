#!/usr/bin/python3
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import matplotlib.animation as animation



def box_collider(x, v):
    if x[0]<=0 or x[0]>=1:
        v[0]=-v[0]
    if x[1]<=0 or x[1]>=1:
        v[1]=-v[1]
    return v

def norm(x):
    return np.sqrt(np.dot(x,x))

class ball:
    def __init__(self, x0, v0, r):
        self.x = np.array(x0)
        self.v = np.array(v0)
        self.r = r
    def colision(self, b_list, m, i):
        for b, j in zip(b_list, range(len(b_list))):
            if m[i,j]==0:
                if norm(self.x-b.x)<=2*self.r:
                    m[i,j]=1
                    m[j,i]=1
                    v = self.v
                    self.v = b.v
                    b.v = v
    def plot(self, ax):
        self.dot = Circle(self.x, self.r)
        ax.add_artist(self.dot)

class dinamic:
    def __init__(self, b_list, h, fps):
        self.step_skip = max(1, round(1/(fps*h)))
        self.fixed_fps = 1/(self.step_skip*h)
        self.interval = 1000/self.fixed_fps
        self.h = h
        self.size = len(b_list)
        self.b_list = b_list
        self.m = np.diag(np.full(self.size,1))
    def step(self):
        for b, i in zip(self.b_list, range(self.size)):
            b.v = box_collider(b.x, b.v)
            b.colision(self.b_list, self.m, i)
            b.x = b.x+self.h*b.v
        self.m = np.diag(np.full(self.size, 1))
    def fixed_step(self):
        for i in range(self.step_skip):
            self.step()
    def plot_update(self):
        for b in self.b_list:
            b.dot.set_center(b.x)
            b.dot.set_color((min(1,2*norm(b.v)),0.6,1))

L = 5
t_final = 60
h = 0.005
fps = 30
t = np.arange(0,t_final,h)

b_list = []

fig, ax = plt.subplots()
ax.set(xlim=[0,1], ylim=[0,1], aspect="equal", xticks=[], yticks=[])

s = np.linspace(0.1,0.9, L)
x = []
for si in s:
    for sj in s:
        x.append(np.array([si, sj]))

for i in range(L**2):
    b = ball(x[i]+0.1*np.random.rand(), 0.4*np.random.rand(2), r=0.02)
    b.plot(ax)
    b_list.append(b)

state = dinamic(b_list, h, fps)

def update(i):
    global state
    state.fixed_step()
    state.fixed_step()
    state.plot_update()


args_animation = {
            "fig":fig,
            "func":update,
            "frames":t[::state.step_skip].size,
            "interval":state.interval,
        }

ani = animation.FuncAnimation(**args_animation)
ani.save("media/colision.gif", writer="ffmpeg")


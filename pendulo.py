#!/usr/bin/python3
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import matplotlib.animation as animation

t_final = 30
h = 0.01
t = np.arange(0,t_final,h)

fps = 60
skip=max(1, round(1/(fps*h)))
fixed_fps = 1/(skip*h)
interval = 1000/fixed_fps 

alpha0 = -0.5*np.pi
omega0 = 0
g, l = 9.78, 1
k = g/l
b = 0.05

def f(alpha, omega):
    return -k*np.sin(alpha)-b*omega

def euler_step(alpha, omega, h):
    omega1 = omega+h*f(alpha, omega)
    alpha1 = alpha+h*omega
    omega2 = omega1+h*f(alpha1, omega1)
    omega = 0.5*(omega1+omega2)
    alpha = alpha+h*omega
    return alpha, omega

x, y = [], []

alpha, omega = alpha0, omega0
for ti in t:
    x.append(np.sin(alpha))
    y.append(-np.cos(alpha))
    alpha, omega = euler_step(alpha, omega, h)

x = np.array(x[::skip])
y = np.array(y[::skip])

fig, ax = plt.subplots()
ax.plot([-0.2,-0.05,0.05,0.2],[-1.1,0.05,0.05,-1.1], color="black", linewidth=1.8,alpha=0.4)
line, = ax.plot([0,np.sin(alpha)],[0,-np.cos(alpha)],color="gray",linewidth=0.8)
ax.plot([0],[0],marker="o",color="black",alpha=0.4)
dot = Circle((x[0],y[0]), 0.1,color=(0,0.6,1))
ax.add_artist(dot)
ax.set(xlim=[-1.1,1.1], ylim=[-1.1,0.1],aspect="equal",xticks=[],yticks=[])


def update(i,x,y):
    line.set_xdata([0,x[i]])
    line.set_ydata([0,y[i]])
    dot.set_center((x[i],y[i]))
    
args_animation = {
            "fig":fig,
            "func":update,
            "fargs":(x,y),
            "frames":x.size,
            "interval":interval,
        }
ani = animation.FuncAnimation(**args_animation)
ani.save("media/pendulo.gif", writer="ffmpeg", dpi=200)

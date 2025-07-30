import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Rectangle

L = 8
x = np.random.choice([0,1], L*L, p=[0.5,0.5]).reshape(L,L)

labels = np.zeros_like(x)
history = [labels.copy()]
max_label = 0 
def get_value(i,j):
    if i>=0 and j>=0:
        if x[i,j]==1:
            return True
    return False
for i in range(L):
    for j in range(L):
        if x[i,j]==0:
            continue
        if get_value(i-1,j) and get_value(i,j-1):
            label1 = min(labels[i-1,j],labels[i,j-1])
            label2 = max(labels[i-1,j],labels[i,j-1])
            if label1!=label2:
                labels[labels==label2]=label1
                labels[labels>label2]=labels[labels>label2]-1
            max_label = labels.max()
            labels[i,j]=label1
        elif get_value(i-1,j) and not get_value(i,j-1):
            labels[i,j]=labels[i-1,j]
        elif get_value(i,j-1) and not  get_value(i-1,j):
            labels[i,j]=labels[i,j-1]
        else:
            max_label = max_label+1
            labels[i,j]=max_label 
        history.append(labels.copy())

fig, (ax1, ax2) = plt.subplots(1,2)

colors = [
    "red",
    "blue",
    "green",
    "orange",
    "purple",
    "cyan",
    "magenta",
    "yellow",
    "black",
    "gray",
    "brown",
    "pink"
]

def plot(x,ax):
    ax.clear()
    ax.set(xlim=[0,L],ylim=[0,L],aspect="equal")
    ax.set_xticks(np.arange(L+1))
    ax.set_yticks(np.arange(L+1))
    ax.invert_yaxis()
    ax.grid(True)
    for i in range(L):
        for j in range(L):
            if x[i,j]>0:
                rec = Rectangle((j,i),1,1,fc=colors[x[i,j]])
            else:
                rec = Rectangle((j,i),1,1,fc="white")
            ax.add_artist(rec)

def update(i, history, x, ax1, ax2):
    plot(history[i], ax2)
    plot(x, ax1)

args_animation = {
            "fig":fig,
            "func":update,
            "fargs":(history, x, ax1 ,ax2),
            "frames":len(history),
            "interval":500,
        }

ani = animation.FuncAnimation(**args_animation)
ani.save("media/cluster.gif", writer="ffmpeg", dpi=200)

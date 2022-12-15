import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

x = [200, 300, 400, 500]
y = [500, 400, 300, 200]


fig = plt.figure()
plt.xlim(0, 1000)
plt.ylim(0, 1000)
plt.gca().invert_yaxis()
(graph,) = plt.plot([], [], "o")


def animate(i):
    graph.set_data(x[: i + 1], y[: i + 1])
    return graph


ani = FuncAnimation(fig, animate, frames=10, interval=200, repeat=True)

plt.show()

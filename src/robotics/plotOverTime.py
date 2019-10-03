import time
import matplotlib.pyplot as plt
import csv
import numpy as np


f = open('test1.csv')
csv_f = list(csv.reader(f))

plt.ion()

fig, ax = plt.subplots()
x, y = [float(csv_f[0][1])], [float(csv_f[0][2])]
xd, yd = [float(csv_f[0][4])], [float(csv_f[0][5])]
sc = ax.scatter(x, y)
plt.xlim(0, 80)
plt.ylim(0, 80)
plt.title("Nonlinear Pose Estimation (Blue) vs Trajectory(Orange)")
plt.xlabel("x (inches)")
plt.ylabel("y (inches)")
plt.draw()


i = 0
for row in csv_f:
    i += 1
    timeToSleep = float(csv_f[i][0]) - float(csv_f[i-1][0])
    plt.pause(timeToSleep)

    x.append(float(csv_f[i][1]))
    y.append(float(csv_f[i][2]))

    xd.append(float(csv_f[i][4]))
    yd.append(float(csv_f[i][5]))

    plt.scatter(x, y, color='orange')
    plt.scatter(xd, yd, color='blue')

    fig.canvas.draw_idle()

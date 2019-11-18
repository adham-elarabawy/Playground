import functions as m
import math
import matplotlib.pyplot as plt
import numpy

# -- CONFIG -- #
increment = 0.2
dt = 0.1
upper_bound = 4  # purely visual, doesn't affect algorithm
lower_bound = -upper_bound
starting_point = 0.5  # keep within upper and lower bounds


# 30 linearly spaced numbers
o_x = numpy.linspace(lower_bound, upper_bound, 300)
o_y = [m.y1(val) for val in o_x]

x = starting_point
y = m.y1(x)

plt.ion()
fig, ax = plt.subplots()
sc = ax.plot(o_x, o_y, c="black")
scp = ax.scatter(x, y, color='#9467bd')
plt.xlim(lower_bound, upper_bound)
plt.ylim(-10, 10)
plt.title("Gradient Descent Visualization")
plt.xlabel("x")
plt.ylabel("y")
plt.draw()
plt.pause(dt)
FINISHED = False

history = []
while not FINISHED:
    y = m.y1(x)
    dy = m.y1_deriv(x)
    print(f'(x,y): ({x},{y})   dy: {dy}', end='\r')
    scp.remove()
    scp = ax.scatter(x, y, color='#9467bd')
    fig.canvas.draw_idle()
    history.append(x)

    if dy > 0:
        x -= increment
    else:
        x += increment
    plt.pause(dt)

    if (len(history) > 1 and x == history[-2]) or dy == 0:
        FINISHED = True

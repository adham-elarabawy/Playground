from sympy import *
import matplotlib.pyplot as plt
import numpy
import random

# -- CONFIG -- #
increment = 0.025
DESCEND = False
kP = 0.05
dt = 0.1
cutoff = 0.001
upper_x = 4  # purely visual, doesn't affect algorithm
lower_x = -upper_x
upper_y = 10
lower_y = -upper_y
starting_point = random.uniform(-2, 2)  # keep within upper and lower bounds

x, y = symbols('x y')
expr = 5*(x**3) - (x**7)
expr_deriv = expr.diff(x)

print(f'Descending? {DESCEND}\nEquation: {expr}\nDerivative: {expr_deriv}')

# original function
o_x = numpy.linspace(lower_x, upper_x, 300)
o_y = [expr.subs(x, val) for val in o_x]

# derivative function
d_x = numpy.linspace(lower_x, upper_x, 300)
d_y = [expr_deriv.subs(x, val) for val in o_x]

curr_x = starting_point
curr_y = expr.subs(x, curr_x)

plt.ion()
fig, ax = plt.subplots()
sc = ax.plot(d_x, d_y, c="grey")
sc = ax.plot(o_x, o_y, c="black")
scp = ax.scatter(curr_x, curr_y, color='#9467bd')
plt.xlim(lower_x, upper_x)
plt.ylim(lower_y, upper_y)
plt.title("Gradient Descent Visualization")
plt.xlabel("x")
plt.ylabel("y")
plt.draw()
plt.pause(dt)
FINISHED = False

history = []
while not FINISHED:
    curr_y = expr.subs(x, curr_x)
    dy = expr_deriv.subs(x, curr_x)
    print(
        f'(x,y): ({round(curr_x, 4)},{round(curr_y, 4)})   dy: {round(dy, 4)}', end='\r')
    scp.remove()
    scp = ax.scatter(curr_x, curr_y, color='#9467bd')
    fig.canvas.draw_idle()
    history.append(curr_x)

    if not DESCEND:
        dy *= -1
    if dy > 0:
        curr_x -= increment
    if dy < 0:
        curr_x += increment

    if (len(history) > 1 and curr_x == history[-2]):
        increment = increment/2
        if increment <= cutoff:
            FINISHED = True
    if dy == 0 or curr_x > upper_x or curr_x < lower_x or curr_y > upper_y or curr_y < lower_y:
        FINISHED = True
    plt.pause(dt)

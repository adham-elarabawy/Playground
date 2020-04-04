from sympy import *
import matplotlib.pyplot as plt
import numpy
import random

# -- CONFIG -- #
increment = 0.025
DESCEND = False
kP = 0.1
dt = 0.1
cutoff = 0.0002
scaling_factor = 1/3
upper_x = 5  # purely visual, doesn't affect algorithm
lower_x = -upper_x
upper_y = 30
lower_y = -upper_y
starting_point = 0.3  # keep within upper and lower bounds

x, y = symbols('x y')

# -- TEMP -- #
coeff_1 = 5 # random.randint(5, 15)
coeff_2 = 1 # random.randint(1, 5)
exp_1 = 3 # random.randint(-6, 6)
exp_2 = 8 # random.randint(-2, 7)

expr = coeff_1*((scaling_factor * x)**exp_1) - \
    coeff_2*((scaling_factor * x)**exp_2)
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
    scp.remove()
    scp = ax.scatter(curr_x, curr_y, color='#9467bd')

    fig.canvas.draw_idle()
    history.append(curr_x)

    increment = dy * kP
    if not DESCEND:
        increment *= -1
    if dy > 0:
        curr_x -= increment
    if dy < 0:
        curr_x += increment

    print(
        f'(x,y): ({round(curr_x, 4)},{round(curr_y, 4)})   dy: {round(dy, 4)}   increment: {increment}', end='\r')
    if abs(increment) <= cutoff:
        FINISHED = True
        print(
            f'\nExited gracefully. Converged on: ({curr_x},{curr_y}) as the relative extrema')
    if dy == 0:
        FINISHED = True
        print(
            f'\nExited on perfect minima. Converged on: ({curr_x},{curr_y}) as the relative extrema')
    if curr_x > upper_x or curr_x < lower_x or curr_y > upper_y or curr_y < lower_y:
        FINISHED = True
        print('\nFell out of bounds.')
    plt.pause(dt)

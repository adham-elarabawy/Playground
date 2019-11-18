from sympy import *
import matplotlib.pyplot as plt
import numpy

# -- CONFIG -- #
increment = 0.025
DESCEND = True
kP = 0.05
dt = 0.1
cutoff = 0.001
upper_bound = 4  # purely visual, doesn't affect algorithm
lower_bound = -upper_bound
starting_point = -1  # keep within upper and lower bounds

x, y = symbols('x y')
expr = 5*(x**3) - (x**7)
expr_deriv = expr.diff(x)

print(f'Descending? {DESCEND}\nEquation: {expr}\nDerivative: {expr_deriv}')

# original function
o_x = numpy.linspace(lower_bound, upper_bound, 300)
o_y = [expr.subs(x, val) for val in o_x]

# derivative function
d_x = numpy.linspace(lower_bound, upper_bound, 300)
d_y = [expr_deriv.subs(x, val) for val in o_x]

curr_x = starting_point
curr_y = expr.subs(x, curr_x)

plt.ion()
fig, ax = plt.subplots()
sc = ax.plot(d_x, d_y, c="grey")
sc = ax.plot(o_x, o_y, c="black")
scp = ax.scatter(curr_x, curr_y, color='#9467bd')
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
    if dy == 0:
        FINISHED = True
    plt.pause(dt)

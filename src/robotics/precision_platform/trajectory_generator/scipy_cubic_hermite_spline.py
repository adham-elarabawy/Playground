import scipy.interpolate as interp
import matplotlib.pyplot as plt
import numpy as np

x_points = np.array([0, 1, 2, 3])
y_points = np.array([12,14,22,39])
dydx_values = np.array([0, 5, 3, 0])

tck = interp.CubicHermiteSpline(x_points, y_points, dydx_values)

x = []
y = []

coeff = {}
for i in range(len(x_points) - 1):
	coeff[i] = []
	x.append(np.linspace(x_points[i], x_points[i + 1], 100))

for order in tck.c:
	for i in range(len(x_points) - 1):
		coeff[i].append(order[i])

print(coeff)

for seg in coeff:
	y.append(coeff[seg][0] * (x[seg] - x_points[seg])**3 + coeff[seg][1] * (x[seg] - x_points[seg])**2 + coeff[seg][2] * (x[seg] - x_points[seg]) + coeff[seg][3])

x_s = []
y_s = []

for i in range(len(x)):
	for j in range(len(x[i])):
		x_s.append(x[i][j])
		y_s.append(y[i][j])

plt.plot(x_points, y_points, 'bo')
plt.plot(x_s, y_s)
plt.show()

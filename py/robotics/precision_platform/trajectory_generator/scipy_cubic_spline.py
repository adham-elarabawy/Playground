from scipy import interpolate
import matplotlib.pyplot as plt  

x_points = [ 0, 1, 2, 3, 4, 5]
y_points = [12,14,22,39,58,77]

tck = interpolate.splrep(x_points, y_points, k=3)

print(tck)

plt.plot(x_points, y_points, 'bo', label='data')
plt.show()

def f(x):
    return interpolate.splev(x, tck)

print(f(1.25))
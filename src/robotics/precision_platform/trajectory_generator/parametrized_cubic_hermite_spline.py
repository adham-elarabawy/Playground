import scipy.interpolate as interp
import matplotlib.pyplot as plt
import numpy as np
import math

class ParametrizedCubicHermite:
	def __init__(self, xs, ys, vxs, vys, default_tangent=True):
		
		assert len(xs) == len(ys)
		
		self.xs = xs
		self.ys = ys
		self.vxs = vxs
		self.vys = vys
		self.ts = []
		self.dydxs = None
		self.default_tangent = default_tangent
		
		dist = []
		sum = 0
		for i in range(len(self.xs) - 1):
			hyp = math.sqrt( (self.xs[i] - self.xs[i + 1])**2 + (self.ys[i] - self.ys[i + 1])**2 )
			dist.append(hyp)
			sum = sum + hyp
		dt = 1 / sum
		self.ts.append(0)
		for i in range(len(self.xs) - 1):
			if i == 0:
				self.ts.append(dt * dist[i])
			else:
				self.ts.append(dt * dist[i] + self.ts[i])

	def __init__(self, xs, ys, dydxs, default_tangent=True):

		assert len(xs) == len(ys)

		self.xs = xs
		self.ys = ys
		self.vxs, self.vys, self.ts = [], [], []
		self.dydxs = dydxs
		self.default_tangent = default_tangent

		dist = []
		sum = 0
		for i in range(len(self.xs) - 1):
			hyp = math.sqrt( (self.xs[i] - self.xs[i + 1])**2 + (self.ys[i] - self.ys[i + 1])**2 )
			dist.append(hyp)
			sum = sum + hyp
		dt = 1 / sum
		self.ts.append(0)
		for i in range(len(self.xs) - 1):
			if i == 0:
				self.ts.append(dt * dist[i])
			else:
				self.ts.append(dt * dist[i] + self.ts[i])

		self.vxs.append(1)
		for i in range(len(dydxs)):
			size = math.sqrt((dydxs[i])**2 + 1)
			self.vys.append(dydxs[i] / size)
			if i != 0 and xs[i] > xs[i - 1]:
				self.vxs.append(1 / size)
			elif i != 0:
				self.vxs.append(-1 / size)


	def get_spline(self):
		
		tckx = interp.CubicHermiteSpline(self.ts, self.xs, self.vxs)
		tcky = interp.CubicHermiteSpline(self.ts, self.ys, self.vys)

		coeffx = {}
		coeffy = {}
		t = []

		for i in range(len(self.ts) - 1):
			coeffx[i], coeffy[i] = [], []
			t.append(np.linspace(self.ts[i], self.ts[i + 1], 50))

		for order in tckx.c:
			for i in range(len(self.ts) - 1):
				coeffx[i].append(order[i])

		for order in tcky.c:
			for i in range(len(self.ts) - 1):
				coeffy[i].append(order[i])

		x, y = [], []
		for seg in coeffx:
			x.append(coeffx[seg][0] * (t[seg] - self.ts[seg])**3 + coeffx[seg][1] * (t[seg] - self.ts[seg])**2 + coeffx[seg][2] * (t[seg] - self.ts[seg]) + coeffx[seg][3])
		for seg in coeffy:
			y.append(coeffy[seg][0] * (t[seg] - self.ts[seg])**3 + coeffy[seg][1] * (t[seg] - self.ts[seg])**2 + coeffy[seg][2] * (t[seg] - self.ts[seg]) + coeffy[seg][3])

		x_plot, y_plot = [], []
		for i in range(len(t)):
			for j in range(len(t[i])):
				x_plot.append(x[i][j])
				y_plot.append(y[i][j])

		return (x_plot, y_plot)


	def remove_dydxs_point(self, index):
		self.dydxs.pop(index)

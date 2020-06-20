from gekko import GEKKO
import numpy as np
import matplotlib.pyplot as plt  

xm = np.array([0,1,2,3,4,5])
ym = np.array([0.1,0.2,0.3,0.5,1.0,0.9])

m = GEKKO()
m.x = m.Param(value=np.linspace(0,5))
m.y = m.Var()
m.options.IMODE=2
m.cspline(m.x,m.y,xm,ym)
solution = m.solve(disp=True)
print(m)

p = GEKKO()
p.x = p.Var(value=1,lb=0,ub=5)
p.y = p.Var()
p.cspline(p.x,p.y,xm,ym)
p.Obj(-p.y)
p.solve(disp=False)


plt.plot(xm,ym,'bo',label='data')
plt.plot(m.x.value,m.y.value,'r--',label='cubic spline')
plt.plot(p.x.value,p.y.value,'ko',label='maximum')
plt.legend(loc='best')
plt.show()
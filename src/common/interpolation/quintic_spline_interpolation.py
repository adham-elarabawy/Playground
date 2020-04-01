import math
import numpy as np
import matplotlib.pyplot as plt

class Pose:
    """
    A 2D Pose that contains x,y displacement with heading
    
    ...

    Attributes
    ----------
    x : double
        x position in inches
    y : double
        y position in inches
    theta : 
        angle/heading in radians
    dydx : 
        angle/heading in slope form

    Methods
    -------
    """

    def __init__(self, x, y, theta):
        """
        Parameters
        ----------
        x : double
            x position in inches
        y : double
            y position in inches
        theta : 
            angle/heading in degrees
        """
        self.x = x
        self.y = y
        self.theta = math.radians(theta)
        self.dydx = math.tan(math.radians(theta))

class QuinticSpline:

    hermite_basis = np.array([[-6, 15, -10, 0, 0, 1],
                              [-3, 8, -6, 0, 1, 0],
                              [-0.5, 1.5, -1.5, 0.5, 0, 0],
                              [6, -15, 10, 0, 0, 0],
                              [-3, 7, -4, 0, 0, 0],
                              [0.5, -1, 0.5, 0, 0, 0]])
                              
    hermite_basis_d = np.array([[0, -30, 60, -30, 0, 0],
                                [0, -15, 32, -18, 0, 1],
                                [0, -2.5, 6, -4.5, 1, 0],
                                [0, 30, -60, 30, 0, 0],
                                [0, -15, 28, -12, 0, 0],
                                [0, 2.5, -4, 1.5, 0, 0]])

    hermite_basis_dd = np.array([[0, 0, -120, 180, -60, 0],
                                 [0, 0, -60, 96, -36, 0],
                                 [0, 0, -10, 18, -9, 1],
                                 [0, 0, 120, -180, 60, 0],
                                 [0, 0, -60, 84, -24, 0],
                                 [0, 0, 10, -12, 3, 0]])
    def __init__(self, pose0, pose1):
        self.pose0 = pose0
        self.pose1 = pose1

        euclidian_distance = math.sqrt((pose1.x - pose0.x)**2 + (pose1.y - pose0.y)**2)

        vx0 = math.cos(pose0.theta) * euclidian_distance
        vx1 = math.cos(pose1.theta) * euclidian_distance
        ax0 = 0
        ax1 = 0

        self.x_control_vector = np.array([pose0.x, vx0, ax0, pose1.x, vx1, ax1])

        vy0 = math.sin(pose0.theta) * euclidian_distance
        vy1 = math.sin(pose1.theta) * euclidian_distance
        ay0 = 0
        ay1 = 0

        self.y_control_vector = np.array([pose0.y, vy0, ay0, pose1.y, vy1, ay1])

    @staticmethod
    def get_hermite_vector(t, d=0):
        assert ((d >= 0) and (d <=2)), "Attempted to evaluate a derivative greater than available hermite basis (or a negative derivative)"
        t_vector = np.array([t**5, t**4, t**3, t**2, t, 1])
        if d == 0 :
            return QuinticSpline.hermite_basis.dot(t_vector)
        if d == 1 :
            return QuinticSpline.hermite_basis_d.dot(t_vector)
        if d == 2 :
            return QuinticSpline.hermite_basis_dd.dot(t_vector)

    def evaluate(self, t, d=0):
        assert ((d >= 0) and (d <=2)), "Attempted to evaluate a derivative greater than available hermite basis (or a negative derivative)" 
        hermite_vector = QuinticSpline.get_hermite_vector(t, d)
        return np.array([hermite_vector.dot(self.x_control_vector), hermite_vector.dot(self.y_control_vector)])

    


waypoints = [Pose(0,0,0), Pose(10,20,-180)]

spline = QuinticSpline(waypoints[0], waypoints[1])

t = np.linspace(0, 1, num=100)
x, y = [], []
for step in t:
    point = spline.evaluate(step, 0)
    x.append(point[0])
    y.append(point[1])

plt.plot(x, y)
plt.xlabel('x (inches)')
plt.ylabel('y (inches)')
plt.title('Quintic Hermite Spline Interpolation')
plt.show()

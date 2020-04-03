import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad

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
        self.x = x
        self.y = y
        self.theta = math.radians(theta)
        self.dydx = math.tan(math.radians(theta))

class QuinticSpline:
    """
    An individual quintic hermite spline
    
    ...

    Attributes
    ----------
    pose0 : Pose
        2D Pose for the 0th point in the spline
    pose1 : Pose
        2D Pose for the 1th point in the spline
    x_control_vector : numpy array
        vector (length 6) describing: initial x pos, initial x vel, initial x accel, final x pos, final x vel, final x accel
    y_control_vector : numpy array
        vector (length 6) describing: initial y pos, initial y vel, initial y accel, final y pos, final y vel, final y accel

    Methods
    -------
    """

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

    def __init__(self, pose0, pose1, safety_scaling=1.3):
        self.pose0 = pose0
        self.pose1 = pose1
        self.safety_scaling = 1

        euclidian_distance = safety_scaling * math.sqrt((pose1.x - pose0.x)**2 + (pose1.y - pose0.y)**2)

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
        """returns the hermite vector of length 6: [h0(t), h1(t), h2(t), h3(t), h4(t), h5(t)] with each element evaluated at t"""
        assert ((d >= 0) and (d <= 2)), "Attempted to evaluate a derivative greater than available hermite basis (or a negative derivative)"
        assert ((t >= 0) and (t <= 1)), "Attempted to extrapolate out of the region of spline"
        t_vector = np.array([t**5, t**4, t**3, t**2, t, 1])
        if d == 0 :
            return QuinticSpline.hermite_basis.dot(t_vector)
        if d == 1 :
            return QuinticSpline.hermite_basis_d.dot(t_vector)
        if d == 2 :
            return QuinticSpline.hermite_basis_dd.dot(t_vector)

    def evaluate(self, t, d=0):
        """returns the point on the trajectory by evaluating x(t) and y(t) at provided t parameter value (0<=t<=1)"""
        assert ((d >= 0) and (d <= 2)), "Attempted to evaluate a derivative greater than available hermite basis (or a negative derivative)"
        assert ((t >= 0) and (t <= 1)), "Attempted to extrapolate out of the region of spline"
        hermite_vector = QuinticSpline.get_hermite_vector(t, d)
        return np.array([hermite_vector.dot(self.x_control_vector), hermite_vector.dot(self.y_control_vector)])
    
    def compute_curvature(self, t):
        return ((self.evaluate(t, 1)[0] * self.evaluate(t, 2)[1]) - (self.evaluate(t, 2)[0] * self.evaluate(t, 1)[1])) / (math.sqrt((self.evaluate(t,1)[0]**2 + self.evaluate(t,1)[1]**2)**3))
        
class Path:
    
    def __init__(self, waypoints):
        assert len(waypoints) > 1, "Path cannot be generated with only one waypoint."
        self.waypoints = waypoints
        self.num_waypoints = len(waypoints)

        self.splines = []

        for i, waypoint in enumerate(waypoints):
            if (i < self.num_waypoints - 1):
                self.splines.append(QuinticSpline(waypoints[i], waypoints[i+1]))
    
    def map_parameter(self, t):
        return t * (len(self.splines))

    def get_spline(self, t):
        assert ((t >= 0) and (t <= 1)), "Attempted to extrapolate out of the Path"
        normalized_t = self.map_parameter(t)
        spline_index = int(normalized_t)
        spline_local_t = normalized_t - spline_index

        if spline_index == len(self.splines):
            spline_index = len(self.splines) - 1
            spline_local_t = 1
        
        return self.splines[spline_index], spline_local_t

    def evaluate(self, t, d=0):
        assert ((t >= 0) and (t <= 1)), "Attempted to extrapolate out of the Path"

        spline, local_t = self.get_spline(t)
        return spline.evaluate(local_t, d)

    def compute_curvature(self, t):
        assert ((t >= 0) and (t <= 1)), "Attempted to extrapolate out of the Path"
        
        spline, local_t = self.get_spline(t)
        return spline.compute_curvature(local_t)
    
    def theta(self, t):
        """returns radians"""
        path_deriv = self.evaluate(t, 1)
        dydt = path_deriv[1]
        dxdt = path_deriv[0]
        slope = dydt / dxdt
        
        return math.atan(slope)

    def get_plot_values(self, d=0, resolution = 100):
        t = np.linspace(0, 1, num=resolution)
        x, y= [], []
        for step in t:
            point = self.evaluate(step, d)
            x.append(point[0])
            y.append(point[1])
        return x,y
    
    @staticmethod
    def get_distance_between(point0, point1):
        return math.sqrt((point0[0] - point1[0])**2 + (point0[1] - point1[1])**2)

class Robot:

    def __init__(self, track_width, max_velocity, max_acceleration):
        self.track_width = track_width
        self.max_velocity = max_velocity
        self.max_acceleration = max_acceleration
        self.min_acceleration = -max_acceleration

class Trajectory:

    max_dx = 0.127 * 10
    max_dy = 0.00127 * 10
    max_dtheta = 0.0872 * 37

    def integrand(self, t):
        deriv_point = self.path.evaluate(t, 1)
        dx = deriv_point[0]
        dy = deriv_point[1]
        return math.sqrt((dx)**2 + (dy)**2)

    def __init__(self, robot, path, v_initial=0, v_final=0, a_initial=0, spline_resolution=1000, max_trajectory_time=10, min_trajectory_time=1, optimization_dt=0.1):
        self.robot = robot
        self.path = path
        self.v_initial = v_initial
        self.v_final = v_final
        self.a_initial = a_initial
        self.step_size = 1 / (spline_resolution * len(self.path.splines))
        self.max_trajectory_time = max_trajectory_time
        self.min_trajectory_time = min_trajectory_time
        self.optimization_dt = optimization_dt
        self.total_arc_length = quad(self.integrand, 0, 1)[0]
        self.control_points = []
        self.trajectory = []

        done = False
        t0 = 0
        t1 = 1
        count = 0

        self.control_points.append(t0)
        while not done:
            point0 = self.path.evaluate(t0)
            point1 = self.path.evaluate(t1)
            dx = abs(point1[0] - point0[0])
            dy = abs(point1[1] - point0[1])
            dtheta = abs(self.path.theta(t1) - self.path.theta(t0))


            if (dx <= Trajectory.max_dx) and (dy <= Trajectory.max_dy) and (dtheta <= Trajectory.max_dtheta):
                self.control_points.append(t1)
                if t1 >= 1:
                    done = True
                t0 = t1
                t1 = 1
                count += 1
                # print(t0, end='\r')
            else:
                t1 = (t1 + t0) / 2

        forwardpass = [] # t parameter, velocity on trajectory, acceleration

        # STEP 1: forward pass
        for i, control_point_t in enumerate(self.control_points):
            current_state = [self.path.evaluate(control_point_t), self.path.compute_curvature(control_point_t)] # [[x,y], curvature]
            if control_point_t == 0:
                forwardpass.append([control_point_t, v_initial, self.robot.max_acceleration]) # predecessor
            else:
                forwardpass.append([control_point_t, 0, 0])
                ds = Path.get_distance_between(current_state[0], prev_state[0])

                while True:
                    # vf = sqrt(vi^2 + 2*a*d)
                    max_reachable_velocity = math.sqrt((forwardpass[i-1][1])**2 + 2 * forwardpass[i-1][2] * ds )
                    max_velocity = min(self.robot.max_velocity, max_reachable_velocity)
                    forwardpass[i][1] = max_velocity
                    forwardpass[i][2] = self.robot.max_acceleration


                    if(ds < (10**-6)):
                        break #not sure why?

                    actual_acceleration = (max_velocity**2 - (forwardpass[i-1][1])**2) / (2*ds)

                    if ((actual_acceleration - 10**-6) > self.robot.max_acceleration):
                        forwardpass[i-1][2] = self.robot.max_acceleration
                    else:
                        if actual_acceleration > forwardpass[i-1][2]:
                            forwardpass[i-1][2] = actual_acceleration

                        break

            prev_state = current_state

        backwardpass = []  # t parameter, velocity on trajectory, acceleration

        # STEP 2: backward pass
        for i, (reversed_i, control_point_t) in enumerate(reversed(list(enumerate(self.control_points)))):
            current_state = [self.path.evaluate(control_point_t), self.path.compute_curvature(control_point_t)] # [[x,y], curvature]
            if i == 0:
                backwardpass.append([control_point_t, v_final, self.robot.max_acceleration]) # successor
            else:
                forward_state = forwardpass[reversed_i]
                backwardpass.append([control_point_t, 0, 0])
                ds = Path.get_distance_between(current_state[0], prev_state[0])

                while True:
                    # vf = sqrt(vi^2 + 2*a*d)
                    max_reachable_velocity = math.sqrt((backwardpass[i-1][1])**2 + 2 * backwardpass[i-1][2] * ds)

                    if max_reachable_velocity >= forwardpass[reversed_i][1]:
                        break

                    forwardpass[reversed_i][1] = max_reachable_velocity

                    if(ds < (10**-6)):
                        break #not sure why?

                    actual_acceleration = (max_reachable_velocity**2 - (backwardpass[i-1][1])**2) / (2*ds)

                    if ((actual_acceleration + 10**-6) < self.robot.min_acceleration):
                        backwardpass[i-1][2] = self.robot.min_acceleration
                    else:
                        backwardpass[i-1][2] = actual_acceleration
                        break
            prev_state = current_state
        backwardpass = list(reversed(backwardpass))

        # STEP 3: integrate the constrained states forward in time to get the trajectory states
        self.states = [] # t, velocity, acceleration, curvature
        time = 0 # seconds
        velocity = 0 # inches/second

        for i, control_point_t in enumerate(self.control_points):
            if control_point_t == 0:
                ds = Path.get_distance_between(self.path.evaluate(control_point_t), self.path.evaluate(control_point_t+1))
            else:
                ds = Path.get_distance_between(self.path.evaluate(control_point_t), self.path.evaluate(prev_control_point_t))
            
            accel = (forwardpass[i][1]**2 - velocity**2) / (2 * ds)

            dt = 0
            if i > 0:
                self.states[i-1][2] = accel
                if(abs(accel) > 10**-6):
                    # v_f = v_0 + a*t
                    dt = (forwardpass[i][1] - velocity) / accel
                elif abs(velocity) > 10**-6:
                    # delta_x = v * t
                    dt = ds / velocity
                else:
                    raise RuntimeError

            time += dt
            prev_control_point_t = control_point_t
            velocity = forwardpass[i][1]
            curvature = self.path.compute_curvature(control_point_t)

            self.states.append([control_point_t, velocity, accel, curvature])

        print(self.states)






waypoints = [Pose(0,0,0), Pose(20,20,45), Pose(0,45,180)]
path = Path(waypoints)
robot = Robot(5, 20, 4)
# trajectory = Trajectory(robot, path)
x, y = path.get_plot_values()

plt.plot(x, y)
plt.plot([pose.x for pose in waypoints], [pose.y for pose in waypoints], 'ro')
plt.gca().set_aspect('equal', adjustable='box')
plt.xlim(0,45)
plt.ylim(0,45)
plt.title('Quintic Hermite Spline Interpolation')
plt.show()

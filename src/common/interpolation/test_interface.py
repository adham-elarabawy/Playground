import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad
import time
from quintic_spline_interpolation import Pose, Path, Robot, Trajectory

waypoints = [Pose(0,0,0), Pose(70, 30, 90)]
path = Path(waypoints)
robot = Robot(190 * 0.03937, 20, 5)
trajectory = Trajectory(robot, path)
x, y = path.get_plot_values()

animation = True
save = False # WARNING: IF YOU ENABLE THIS, THE TRAJECTORY VISUALIZATION WILL BE SLOWER THAN IT ACTUALLY IS

if not animation:
    plt.plot(x, y)
    plt.plot([pose.x for pose in waypoints], [pose.y for pose in waypoints], 'ro')
    plt.plot([state.pose.x for state in trajectory.trajectory[0::20]], [state.pose.y for state in trajectory.trajectory[0::20]], 'go')

    plt.plot([state.time for state in trajectory.trajectory], [state.velocity for state in trajectory.trajectory], 'g')
    plt.gca().set_aspect('equal', adjustable='box')
    plt.xlim(0,45)
    plt.ylim(0,45)
    plt.title('Quintic Hermite Spline Interpolation')
    plt.show()
else:
    plt.ion()
    fig, (ax0, ax1) = plt.subplots(2, 1, gridspec_kw={'height_ratios':[12,4]})
    fig.tight_layout()
    ax0.set_aspect('equal')
    sc = ax0.plot(x, y)
    wp = ax0.plot([pose.x for pose in waypoints], [pose.y for pose in waypoints], 'ro')
    scp = ax0.scatter([0], [0], color='#9467bd', zorder=4)
    ax1.set_ylim(0, robot.max_velocity)
    ax0.title.set_text('Quintic Hermite Spline Interpolation')
    ax1.title.set_text('Velocity Profile')
    ax0.set_xlabel("x (inches)")
    ax0.set_ylabel("y (inches)")
    ax1.set_xlabel("time (s)")
    ax1.set_ylabel("velocity (in/second)")
    vt = ax1.plot([state.time for state in trajectory.trajectory], [state.velocity for state in trajectory.trajectory])
    plt.subplots_adjust(top=0.9, bottom=0.1, left=0.1, right = 0.9, hspace=0.5)
    plt.draw()


    start_time = time.time()
    loop_time = 0
    dt = 0.05
    total_trajectory_time = trajectory.trajectory[-1].time
    i = 0
    while loop_time <= total_trajectory_time:
        if save:
            plt.savefig('render/' + str(i) + '.png')
        scp.remove()
        scp = ax0.scatter([trajectory.sample(loop_time).pose.x], [trajectory.sample(loop_time).pose.y], color='#9467bd', zorder=4)
        fig.canvas.draw_idle()
        print(trajectory.sample(loop_time).velocity, end='\r')
        loop_time += dt
        plt.pause(dt)
        i += 1

    print('Total trajectory time: ', total_trajectory_time)
    print('Total animation time: ', (time.time() - start_time))
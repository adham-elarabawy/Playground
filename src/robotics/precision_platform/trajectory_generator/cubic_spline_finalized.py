import math

import matplotlib.pyplot as plt
import numpy as np

show_animation = True



def cubic_polynomials_planner(x_points, y_points, dydx_values, dt):
    """
    cubic polynomial planner
    input
        x_points: x position waypoint list
        y_points: y position waypoint list
    return
        time: time result
        rx: x position result list
        ry: y position result list
        ryaw: yaw angle result list
        rv: velocity result list
        ra: accel result list
        rk: curvature result list
    """

    time, rx, ry, ryaw, rv, ra, rj, rk = [], [], [], [], [], [], [], []
    tck = interp.CubicHermiteSpline(x_points, y_points, dydx_values)
    deriv = tck.derivative()

    px, py, vx, vy, k = [], [], [], [], []

    for t in np.arange(0.0, T + dt, dt):
        time.append(t)
        rx.append(xqp.calc_point(t))
        ry.append(yqp.calc_point(t))

        vx = xqp.calc_first_derivative(t)
        vy = yqp.calc_first_derivative(t)
        v = np.hypot(vx, vy)
        yaw = math.atan2(vy, vx)
        rv.append(v)
        ryaw.append(yaw)

        ax = xqp.calc_second_derivative(t)
        ay = yqp.calc_second_derivative(t)
        a = np.hypot(ax, ay)
        if len(rv) >= 2 and rv[-1] - rv[-2] < 0.0:
            a *= -1
        ra.append(a)

        jx = xqp.calc_third_derivative(t)
        jy = yqp.calc_third_derivative(t)
        j = np.hypot(jx, jy)
        if len(ra) >= 2 and ra[-1] - ra[-2] < 0.0:
            j *= -1
        rj.append(j)

        k = abs((vx*ay) - (vy*ax)) / (((vx**2) + (vy**2))**(3/2))
        rk.append(k)

        if max([abs(i) for i in ra]) <= max_accel and max([abs(i) for i in rj]) <= max_jerk:
            print("find path!!")
            break

    if show_animation:  # pragma: no cover
        for i, _ in enumerate(time):
            plt.cla()
            # for stopping simulation with the esc key.
            plt.gcf().canvas.mpl_connect('key_release_event',
                                         lambda event: [exit(0) if event.key == 'escape' else None])
            plt.grid(True)
            plt.axis("equal")
            plot_arrow(sx, sy, syaw)
            plot_arrow(gx, gy, gyaw)
            plot_arrow(rx[i], ry[i], ryaw[i])
            plt.title("Time[s]:" + str(time[i])[0:4] +
                      " v[in/s]:" + str(rv[i])[0:4] +
                      " a[in/ss]:" + str(ra[i])[0:4] +
                      " curvature[rad/in]:" + str(rk[i])[0:4],
                      )
            plt.pause(0.001)

    return time, rx, ry, ryaw, rv, ra, rk


def plot_arrow(x, y, yaw, length=1.0, width=0.5, fc="r", ec="k"):  # pragma: no cover
    """
    Plot arrow
    """

    if not isinstance(x, float):
        for (ix, iy, iyaw) in zip(x, y, yaw):
            plot_arrow(ix, iy, iyaw)
    else:
        plt.arrow(x, y, length * math.cos(yaw), length * math.sin(yaw),
                  fc=fc, ec=ec, head_width=width, head_length=width)
        plt.plot(x, y)


def main():
    print(__file__ + " start!!")

    sx = 10.0  # start x position [in]
    sy = 10.0  # start y position [in]
    syaw = np.deg2rad(0.0)  # start yaw angle [rad]
    sv = 5  # start speed [in/s]
    sa = 0.1  # start accel [in/ss]
    gx = 76.0  # goal x position [in]
    gy = 20.0  # goal y position [in]
    gyaw = np.deg2rad(180.0)  # goal yaw angle [rad]
    gv = 5  # goal speed [in/s]
    ga = 0.1  # goal accel [in/ss]
    max_accel = 7.0  # max accel [in/ss]
    max_jerk = 0.3  # max jerk [in/sss]
    dt = 0.1  # time tick [s]

    time, x, y, yaw, v, a, k = quintic_polynomials_planner(
        sx, sy, syaw, sv, sa, gx, gy, gyaw, gv, ga, max_accel, max_jerk, dt)

    print(str(x))
    print(str(y))

    if show_animation:  # pragma: no cover
        plt.plot(x, y, "-r")

        plt.subplots()
        plt.plot(time, [np.rad2deg(i) for i in yaw], "-r")
        plt.xlabel("Time[s]")
        plt.ylabel("Yaw[deg]")
        plt.grid(True)

        plt.subplots()
        plt.plot(time, v, "-r")
        plt.xlabel("Time[s]")
        plt.ylabel("Speed[in/s]")
        plt.grid(True)

        plt.subplots()
        plt.plot(time, a, "-r")
        plt.xlabel("Time[s]")
        plt.ylabel("accel[in/ss]")
        plt.grid(True)

        plt.subplots()
        plt.plot(time, k, "-r")
        plt.xlabel("Time[s]")
        plt.ylabel("curvature[rad/in]")
        plt.grid(True)

        plt.show()



if __name__ == '__main__':
    main()
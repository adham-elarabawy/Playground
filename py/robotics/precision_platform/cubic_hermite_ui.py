from scipy import interpolate as interp
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.widgets import Button
import trajectory_generator.parametrized_cubic_hermite_spline as spline_generator
import trajectory_generator.draggable_points as draggable_points

def add_point(event):
    global dr, ax, c_spline

    if dr.setting_tangent:
        return
    
    dr.add_point(event)
    dr = draggable_points.DraggablePoints(dr.artists, ax, plt)
    c_spline.dydxs.append(0)

def remove_point(event):
    global dr, ax, c_spline

    if not dr.setting_tangent:
        c_spline.remove_dydxs_point(dr.current_index)
        dr.remove_point(event)
        dr = draggable_points.DraggablePoints(dr.artists, ax, plt)
    else:
        dr.tangent_point.remove()
        dr.tangent_point = None
        dr = draggable_points.DraggablePoints(dr.artists, ax, plt, setting_tangent=dr.setting_tangent)
        plt.draw()

def edit_tangent(event):
    global dr, ax, c_spline

    dr.setting_tangent = not dr.setting_tangent
    if not dr.setting_tangent:
        if dr.tangent_point is not None:
            dr.tangent_point.remove()
            dr.tangent_point = None
            dr = draggable_points.DraggablePoints(dr.artists, ax, plt)
            plt.draw()
    #TODO: check tangent editing

def reset_tangent(event):
    global c_spline

    c_spline.default_tangent = True

def on_mouse_move(event):
    global dr, c_spline

    if dr.currently_dragging and not (dr.current_artist == None):
        if c_spline.default_tangent:
            c_spline.dydxs = []
            c_spline.dydxs.append(0)
            for i in range(len(dr.xs) - 2):
                c_spline.dydxs.append((dr.artists[i].get_center()[1] - dr.artists[i + 2].get_center()[1]) / (dr.artists[i].get_center()[0] - dr.artists[i + 2].get_center()[0]))
            c_spline.dydxs.append(0)
        c_spline = spline_generator.ParametrizedCubicHermite(dr.xs, dr.ys, c_spline.dydxs, default_tangent=c_spline.default_tangent)
        spline = c_spline.get_spline()
        ax.plot(spline[0], spline[1], color = 'b')
        if len(ax.lines) > 1:
            ax.lines.remove(ax.lines[0])

    if dr.currently_dragging and dr.setting_tangent:
        if c_spline.default_tangent:
            c_spline.dydxs = []
            c_spline.dydxs.append(0)
            for i in range(len(dr.xs) - 2):
                c_spline.dydxs.append((dr.artists[i].get_center()[1] - dr.artists[i + 2].get_center()[1]) / (dr.artists[i].get_center()[0] - dr.artists[i + 2].get_center()[0]))
            c_spline.dydxs.append(0)
        dydx = (dr.current_artist.get_center()[1] - event.ydata) / (dr.current_artist.get_center()[0] - event.xdata)
        c_spline.dydxs[dr.current_index] = dydx
        c_spline = spline_generator.ParametrizedCubicHermite(dr.xs, dr.ys, c_spline.dydxs, default_tangent=c_spline.default_tangent)
        spline = c_spline.get_spline()
        ax.plot(spline[0], spline[1], color = 'b')
        if len(ax.lines) > 1:
            ax.lines.remove(ax.lines[0])
        c_spline.default_tangent = False


if __name__ == '__main__':
    fig, ax = plt.subplots()
    ax.set(xlim=[-1, 2], ylim=[-1, 2])
    points = [plt.Circle((0.3, 0.3), 0.03, color = 'r'), plt.Circle((0.32, 0.3), 0.03, color = 'r')]
    for point in points:
        ax.add_artist(point)
    dr = draggable_points.DraggablePoints(points, ax, plt)
    c_spline = spline_generator.ParametrizedCubicHermite(dr.xs, dr.ys, [0, 0])
    apointadd = plt.axes([0.81, 0.02, 0.06, 0.035])
    bpointadd = Button(apointadd, 'Add')
    bpointadd.on_clicked(add_point)
    apointremove = plt.axes([0.66, 0.02, 0.09, 0.035])
    bpointremove = Button(apointremove, 'Remove')
    bpointremove.on_clicked(remove_point)
    atangent = plt.axes([0.28, 0.02, 0.09, 0.035])
    btangent = Button(atangent, 'Tangent')
    btangent.on_clicked(edit_tangent)
    adefault = plt.axes([0.44, 0.02, 0.17, 0.035])
    bdefault = Button(adefault, 'Reset Tangent')
    bdefault.on_clicked(reset_tangent)
    plt.connect('motion_notify_event', on_mouse_move)
    plt.gcf().canvas.mpl_connect('key_release_event',
                                lambda event: [exit(0) if event.key == 'escape' else None])
    plt.show()
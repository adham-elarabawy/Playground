class DraggablePoints(object):
    def __init__(self, artists, ax, plt, tolerance=20, setting_tangent=False):
        for artist in artists:
            artist.set_picker(tolerance)
        self.artists = artists
        self.currently_dragging = False
        self.current_artist = None
        self.last_circle = None
        self.current_index = None
        self.offset = (0, 0)
        self.xs, self.ys = [], []
        self.tangent_point = None
        self.setting_tangent = setting_tangent
        self.ax = ax
        self.plt = plt
        for artist in artists:
            self.xs.append(artist.get_center()[0])
            self.ys.append(artist.get_center()[1])
            artist.set_facecolor('r')
            artist.set_edgecolor('r')
        for canvas in set(artist.figure.canvas for artist in self.artists):
            canvas.mpl_connect('button_press_event', self.on_press)
            canvas.mpl_connect('button_release_event', self.on_release)
            canvas.mpl_connect('pick_event', self.on_pick)
            canvas.mpl_connect('motion_notify_event', self.on_motion)
    def on_press(self, event):
        if (self.current_artist in (self.ax.findobj(match = type(self.plt.Circle(1, 1))))):
            self.current_artist.set_facecolor('g')
            self.current_artist.set_edgecolor('g')
            self.current_artist.figure.canvas.draw()
            self.last_circle = self.current_artist
        self.currently_dragging = True
    def on_release(self, event):
        self.currently_dragging = False
        if self.current_artist is not None and not self.setting_tangent:
            self.current_artist.set_edgecolor('r')
            self.current_artist.set_facecolor('r')
            self.current_artist = None
            #self.current_index = None
    def on_pick(self, event):
        if self.current_artist is not None and self.setting_tangent:
            self.current_artist.set_edgecolor('r')
            self.current_artist.set_facecolor('r')
        if self.current_artist is None or self.setting_tangent:
            x0, y0 = event.artist.center
            x1, y1 = event.mouseevent.xdata, event.mouseevent.ydata
            self.offset = (x0 - x1), (y0 - y1)
            self.current_artist = event.artist
            #if event.artist is None:
            for i in range(len(self.xs)):
                if self.xs[i] == x0:
                    self.current_index = i
                    break
            if self.setting_tangent and self.tangent_point is None:
                self.tangent_point = self.plt.Circle(event.artist.get_center(), event.artist.get_radius(), color = 'y')
                self.ax.add_artist(self.tangent_point)
                self.tangent_point.figure.canvas.mpl_connect('button_press_event', self.on_press)
                self.tangent_point.figure.canvas.mpl_connect('button_release_event', self.on_release)
                self.tangent_point.figure.canvas.mpl_connect('pick_event', self.on_pick)
                self.tangent_point.figure.canvas.mpl_connect('motion_notify_event', self.on_motion)
    def on_motion(self, event):
        if not self.currently_dragging:
            return
        if self.current_artist is None and self.tangent_point is None:
            return
        dx, dy = self.offset
        if not self.setting_tangent:
            self.current_artist.center = event.xdata + dx, event.ydata + dy
            self.current_artist.figure.canvas.draw()
            self.xs[self.current_index] = event.xdata + dx
            self.ys[self.current_index] = event.ydata + dy
        else:
            self.tangent_point.center = event.xdata + dx, event.ydata + dy
            self.tangent_point.figure.canvas.draw()
    def add_point(self, event):
        new_point = self.plt.Circle((0.32, 0.3), 0.03, color = 'r')
        self.artists.append(new_point)
        self.ax.add_artist(new_point)
        self.plt.draw()
        self.setting_tangent = False
    def remove_point(self, event):
        self.last_circle.remove()
        self.artists.remove(self.last_circle)
        self.setting_tangent = False
#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_gtk4agg import FigureCanvas # gtk4cairo or gtk4agg
from matplotlib.backends.backend_gtk4 import NavigationToolbar2GTK4 as NavigationToolbar

class MyApp(Gtk.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect('activate', self.on_activate)

    # When the application is launched…
    def on_activate(self, app):
        builder = Gtk.Builder()
        builder.add_from_file("src/ui/camada.ui")

        ## matplot chart / graph
        fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, dpi=100)

        T = 3           # max time shown on this window (s)
        Fs = 500        # sampling frequency (Hz)
        x = np.linspace(0, T, int(T * Fs)) # or time axis. Go from 0 upto T with pass 1/(T*Fs)

        y1 = np.sin(2*np.pi*x)
        ax1.plot(x,y1, color='green')
        y2 = np.cos(2*np.pi*0.25*x+1.3) - y1
        ax1.plot(x,y2, color='darkblue')
        y3 = np.cos(2*np.pi*x)
        y4_square_wave = np.where(np.mod(np.floor(2* 0.006 * Fs * x), 2) == 0, 1, -1)
        ax2.plot(x,y3, color='red')
        ax2.plot(x,y4_square_wave, label='square wave')
        ax2.set_ylabel('YLabel')
        ax2.set_xlabel('XLabel')
        ax2.legend(loc='upper right')
        ax2.set_title('Sinusoidal and square signals')

        figCanvas = FigureCanvas(fig) # a Gtk.DrawingArea
        figCanvas.set_size_request(600,400)
        navBar = NavigationToolbar(figCanvas)
        #navBar.set_valign(Gtk.Align.CENTER)
        ## end graph

        previewBox = builder.get_object("preview")
        previewBox.append(figCanvas)
        previewBox.append(navBar)

        self.win = builder.get_object("mainWindow")
        self.win.set_application(self)  # Application will close if it has no active windows attached to it
        self.win.present()

# Create and run a new application
app = MyApp(application_id='com.gitlab.camada')
app.run(None)

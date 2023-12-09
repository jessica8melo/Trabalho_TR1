#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_gtk4agg import FigureCanvas # gtk4cairo or gtk4agg
from matplotlib.backends.backend_gtk4 import NavigationToolbar2GTK4 as NavigationToolbar
import os.path as path
from camada.fisica import *
from camada.enlace import *
from enum import Enum, auto

class MyApp(Gtk.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect('activate', self.on_activate)
        self.settings = {
            self.Enquadramento: self.Enquadramento.CONTAGEM_CARACTERES,
            self.ModulacaoDigital: self.ModulacaoDigital.NRZ_POLAR,
            self.ModulacaoPortadora: []
        }

    class Enquadramento(Enum):
        CONTAGEM_CARACTERES = auto()
        INSERCAO_BITS = auto()

    class ModulacaoDigital(Enum):
        NRZ_POLAR = auto()
        MANCHESTER = auto()
        BIPOLAR = auto()

    class ModulacaoPortadora(Enum):
        ASK = auto()
        FSK = auto()
        _8QAM = auto()

    def on_submit(self, widget, app):
        txtBuffer = self.entryTemDeBits.get_buffer()
        print(txtBuffer.get_text())

    def on_toggle_enquadramento(self, widget, tipoEnquadramento):
        self.settings[self.Enquadramento] = tipoEnquadramento
        print(self.settings[self.Enquadramento])

    def on_toggle_mDigital(self, widget, tipoModulacao):
        self.settings[self.ModulacaoDigital] = tipoModulacao
        print(self.settings[self.ModulacaoDigital])

    def on_toggle_mPortadora(self, widget, tipoModulacao):
        if tipoModulacao not in self.settings[self.ModulacaoPortadora]:
            self.settings[self.ModulacaoPortadora].append(tipoModulacao)
        else:
            self.settings[self.ModulacaoPortadora].remove(tipoModulacao)
        print(self.settings[self.ModulacaoPortadora])

    # When the application is launched…
    def on_activate(self, app):
        builder = Gtk.Builder()
        builder.add_from_file(path.join(path.dirname(__file__) , "ui/camada.ui"))

        # get objects reference
        self.win = builder.get_object("winMain")
        self.entryTemDeBits = builder.get_object("entryTemDeBits")
        self.chkBtnContagemCaracteres = builder.get_object("chkBtnContagemCaracteres")
        self.chkBtnInsercaoBits = builder.get_object("chkBtnInsercaoBits")
        self.chkBtnNRZPolar = builder.get_object("chkBtnNRZPolar")
        self.chkBtnManchester = builder.get_object("chkBtnManchester")
        self.chkBtnBipolar = builder.get_object("chkBtnBipolar")
        self.chkBtnASK = builder.get_object("chkBtnASK")
        self.chkBtnFSK = builder.get_object("chkBtnFSK")
        self.chkBtn8QAM = builder.get_object("chkBtn8QAM")
        self.btnSubmit = builder.get_object("btnSubmit")
        boxPreview = builder.get_object("boxPreview")

        # connect signals
        self.chkBtnContagemCaracteres.connect("toggled", self.on_toggle_enquadramento, self.Enquadramento.CONTAGEM_CARACTERES)
        self.chkBtnInsercaoBits.connect("toggled", self.on_toggle_enquadramento, self.Enquadramento.INSERCAO_BITS)
        self.chkBtnManchester.connect("toggled", self.on_toggle_mDigital, self.ModulacaoDigital.MANCHESTER)
        self.chkBtnBipolar.connect("toggled", self.on_toggle_mDigital, self.ModulacaoDigital.BIPOLAR)
        self.chkBtnNRZPolar.connect("toggled", self.on_toggle_mDigital, self.ModulacaoDigital.NRZ_POLAR)
        self.chkBtnASK.connect("toggled", self.on_toggle_mPortadora, self.ModulacaoPortadora.ASK)
        self.chkBtnFSK.connect("toggled", self.on_toggle_mPortadora, self.ModulacaoPortadora.FSK)
        self.chkBtn8QAM.connect("toggled", self.on_toggle_mPortadora, self.ModulacaoPortadora._8QAM)
        self.btnSubmit.connect("clicked", self.on_submit, app)

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

        self.win.set_application(self)  # Application will close if it has no active windows attached to it
        self.win.present()

# Create and run a new application
app = MyApp(application_id='com.gitlab.camada')
app.run(None)

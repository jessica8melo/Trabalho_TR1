#!/usr/bin/env python3

import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_gtk4agg import FigureCanvas # gtk4cairo or gtk4agg
from matplotlib.backends.backend_gtk4 import NavigationToolbar2GTK4 as NavigationToolbar
import os.path as path
from camada.fisica import *
from camada.enlace import *
from enum import Enum, auto

class MyApp(Gtk.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect("activate", self.on_activate)
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

    def on_submit(self, widget):
        txtBuffer = self.entryTemDeBits.get_buffer()

        # toDo: enquadramento do trem de bits
        if len(txtBuffer.get_text()) < 1:
            return
        else:
            txtEnquadrado = txtBuffer.get_text()

        match self.settings[self.ModulacaoDigital]:
            case self.ModulacaoDigital.NRZ_POLAR:
                (x, y) = nrz_polar(txtEnquadrado)
            case self.ModulacaoDigital.MANCHESTER:
                (x, y) = manchester(txtEnquadrado)
            case self.ModulacaoDigital.BIPOLAR:
                (x, y) = bipolar(txtEnquadrado)

        # Check if "fig" is defined on self
        if not hasattr(self, "fig"):
            self.fig = Figure(dpi=100)
            self.axModulacaoDigital = self.fig.add_subplot()
            self.axModulacaoDigital.sharex=True

            self.line2d = self.axModulacaoDigital.plot(x, y)
            self.fig.suptitle("Modulação digital")

            figCanvas = FigureCanvas(self.fig)
            figCanvas.set_size_request(600,400)
            navBar = NavigationToolbar(figCanvas)

            self.boxPreview.append(figCanvas)
            self.boxPreview.append(navBar)
        else:
            self.axModulacaoDigital.clear()
            self.axModulacaoDigital.plot(x, y)
            self.fig.canvas.draw()

    def on_toggle_enquadramento(self, widget, tipoEnquadramento):
        self.settings[self.Enquadramento] = tipoEnquadramento
        print(self.settings[self.Enquadramento])

    def on_toggle_mDigital(self, widget, tipoModulacao):
        self.settings[self.ModulacaoDigital] = tipoModulacao

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
        self.boxPreview = builder.get_object("boxPreview")

        # connect signals
        self.chkBtnContagemCaracteres.connect("toggled", self.on_toggle_enquadramento, self.Enquadramento.CONTAGEM_CARACTERES)
        self.chkBtnInsercaoBits.connect("toggled", self.on_toggle_enquadramento, self.Enquadramento.INSERCAO_BITS)
        self.chkBtnNRZPolar.connect("toggled", self.on_toggle_mDigital, self.ModulacaoDigital.NRZ_POLAR)
        self.chkBtnManchester.connect("toggled", self.on_toggle_mDigital, self.ModulacaoDigital.MANCHESTER)
        self.chkBtnBipolar.connect("toggled", self.on_toggle_mDigital, self.ModulacaoDigital.BIPOLAR)
        self.chkBtnASK.connect("toggled", self.on_toggle_mPortadora, self.ModulacaoPortadora.ASK)
        self.chkBtnFSK.connect("toggled", self.on_toggle_mPortadora, self.ModulacaoPortadora.FSK)
        self.chkBtn8QAM.connect("toggled", self.on_toggle_mPortadora, self.ModulacaoPortadora._8QAM)
        self.btnSubmit.connect("clicked", self.on_submit)

        self.win.set_application(self)  # Application will close if it has no active windows attached to it
        self.win.present()

# Create and run a new application
app = MyApp(application_id="com.github.jessica8melo.Trabalho_TR1")
app.run(None)

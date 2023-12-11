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
    QAM_8 = auto()

class MyApp(Gtk.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect("activate", self.on_activate)
        self.settings = {
            Enquadramento: Enquadramento.CONTAGEM_CARACTERES,
            ModulacaoDigital: ModulacaoDigital.NRZ_POLAR,
            ModulacaoPortadora: []
        }

    def graph_canvas_update(self, widget):
        txtBuffer = self.entryTemDeBits.get_buffer()

        # toDo: enquadramento do trem de bits
        if len(txtBuffer.get_text()) < 1:
            return
        else:
            txtEnquadrado = txtBuffer.get_text()

        # Calc digital modulation
        match self.settings[ModulacaoDigital]:
            case ModulacaoDigital.NRZ_POLAR:
                yMD = nrz_polar(txtEnquadrado)
            case ModulacaoDigital.MANCHESTER:
                yMD = manchester(txtEnquadrado)
            case ModulacaoDigital.BIPOLAR:
                yMD = bipolar(txtEnquadrado)

        # Calc analog modulation
        for item in self.settings[ModulacaoPortadora]:
            match item:
                case ModulacaoPortadora.ASK:
                    yASK = ask(txtEnquadrado)
                case ModulacaoPortadora.FSK:
                    yFSK = fsk(txtEnquadrado)
                case ModulacaoPortadora.QAM_8:
                    yQAM_8 = qam_8(txtEnquadrado)

        # Define the x-axis for all axes (graphs)
        x = np.arange(0,len(txtEnquadrado),.01)

        # Check if "fig" is defined on self
        if hasattr(self, "fig"):
            # Clear graphs axes
            self.axModulacaoDigital.clear()
            self.axModulacaoPortadora.clear()

            self.axModulacaoDigital.set_title("Digital")
            self.axModulacaoPortadora.set_title("Analógica")
            self.axModulacaoDigital.sharex = True
            self.axModulacaoPortadora.sharex = True

            # Make sure variable is defined locally and
            # has a value. Then, plot on axes
            if "yMD" in locals() and yMD is not None:
                self.axModulacaoDigital.plot(x, yMD)
            if "yASK" in locals() and yASK is not None:
                self.axModulacaoPortadora.plot(x, yASK)
            if "yFSK" in locals() and yFSK is not None:
                self.axModulacaoPortadora.plot(x, yFSK)
            if "yQAM_8" in locals() and yQAM_8 is not None:
                self.axModulacaoPortadora.plot(x, yQAM_8)

            # Draw changes on axes into canvas
            self.fig.canvas.draw()

    def on_toggle_enquadramento(self, widget, tipoEnquadramento):
        self.settings[Enquadramento] = tipoEnquadramento
        self.graph_canvas_update(widget)

    def on_toggle_mDigital(self, widget, tipoModulacao):
        self.settings[ModulacaoDigital] = tipoModulacao
        self.graph_canvas_update(widget)

    def on_toggle_mPortadora(self, widget, tipoModulacao):
        if tipoModulacao not in self.settings[ModulacaoPortadora]:
            self.settings[ModulacaoPortadora].append(tipoModulacao)
        else:
            self.settings[ModulacaoPortadora].remove(tipoModulacao)
        self.graph_canvas_update(widget)

    def graph_canvas_show(self):
        # Check if "fig" is defined on self
        if hasattr(self, "fig"):
            return

        # Create a new figure with 100 dots per inch
        # and set a subscript title
        self.fig = Figure(dpi=100)
        self.fig.suptitle("Modulações", fontsize="x-large", fontweight="bold")
        self.fig.subplots_adjust(top=.85, hspace=.5)

        # Define a new axes to plot digital modulation
        self.axModulacaoDigital = self.fig.add_subplot(2, 1, 1)
        # Define a new axes to plot analog modulation
        self.axModulacaoPortadora = self.fig.add_subplot(2, 1, 2)

        figCanvas = FigureCanvas(self.fig)
        figCanvas.set_size_request(600,400)
        navBar = NavigationToolbar(figCanvas)

        self.boxPreview.append(figCanvas)
        self.boxPreview.append(navBar)

    # When the application is launched…
    def on_activate(self, app):
        builder = Gtk.Builder()
        builder.add_from_file(path.join(path.dirname(__file__) , "ui/camada.ui"))

        # Get objects reference
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

        # Connect signals
        self.chkBtnContagemCaracteres.connect("toggled", self.on_toggle_enquadramento, Enquadramento.CONTAGEM_CARACTERES)
        self.chkBtnInsercaoBits.connect("toggled", self.on_toggle_enquadramento, Enquadramento.INSERCAO_BITS)
        self.chkBtnNRZPolar.connect("toggled", self.on_toggle_mDigital, ModulacaoDigital.NRZ_POLAR)
        self.chkBtnManchester.connect("toggled", self.on_toggle_mDigital, ModulacaoDigital.MANCHESTER)
        self.chkBtnBipolar.connect("toggled", self.on_toggle_mDigital, ModulacaoDigital.BIPOLAR)
        self.chkBtnASK.connect("toggled", self.on_toggle_mPortadora, ModulacaoPortadora.ASK)
        self.chkBtnFSK.connect("toggled", self.on_toggle_mPortadora, ModulacaoPortadora.FSK)
        self.chkBtn8QAM.connect("toggled", self.on_toggle_mPortadora, ModulacaoPortadora.QAM_8)
        self.btnSubmit.connect("clicked", self.graph_canvas_update)

        # Add a canvas where to plot graphs
        self.graph_canvas_show()

        self.win.set_application(self)  # Application will close if it has no active windows attached to it
        self.win.present()

# Create and run a new application
app = MyApp(application_id="com.github.jessica8melo.Trabalho_TR1")
app.run(None)

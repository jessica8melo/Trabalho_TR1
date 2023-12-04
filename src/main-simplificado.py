#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_gtk4agg import FigureCanvas # gtk4cairo or gtk4agg
from matplotlib.backends.backend_gtk4 import NavigationToolbar2GTK4 as NavigationToolbar

# Quando a aplicativo iniciar…
def on_activate(app):
    builder = Gtk.Builder()
    builder.add_from_file("ui/camada.ui")

    ## matplot chart / graph
    fig, ax = plt.subplots()

    x = np.linspace(0, 3, 1500)     # Eixo-x começa em 0 até 3 com 1500 pontos
    y = np.sin(2*np.pi*x)           # Função / Sinal sendo desenhado
    ax.plot(x,y, color='green') 
    
    figCanvas = FigureCanvas(fig)
    figCanvas.set_size_request(600,400)
    ## end graph

    previewBox = builder.get_object("preview")
    previewBox.append(figCanvas)
    previewBox.append(NavigationToolbar(figCanvas))

    win = builder.get_object("mainWindow")
    win.set_application(app)  # App encerra se não pussuir um janela ligado nele
    win.present()

# Cria e executa um app
app = Gtk.Application(application_id='com.gitlab.diogob003.camada')
app.connect('activate', on_activate)
app.run(None)
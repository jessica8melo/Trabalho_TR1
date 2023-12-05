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
    builder.add_from_file("src/ui/camada.ui")

    ## matplot chart / graph
    fig, ax = plt.subplots()

    entrada = "1000110"     
    x = np.arange(0,len(entrada),.01)   
    j = 1
    y = []
    for i in range(0,len(entrada)*100,1):
        if x[i]<j:
            if entrada[j-1] == "1":
                saida = 1
            else:
                saida = -1
            y.append(saida)
        else:
            if entrada[j] == "1":
                saida = 1
            else:
                saida = -1
            y.append(saida)
            j+=1
    print(x)
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

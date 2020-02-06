#!/usr/bin/env python3

# Filename: mpltwidgerbar.py

"""This app is for the Amadeus automation tasks."""

from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QSizePolicy
from PyQt5 import QtCore, QtGui

from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

from matplotlib.figure import Figure
from matplotlib import pyplot as plt
import numpy as np
    
class mpltWidgetBar(QWidget):
    
    def __init__(self, parent = None):

        QWidget.__init__(self, parent)
        
        self.lblTitle = QLabel('Pricing Template counts per Usage Type')
        self.lblTitle.setFont(QtGui.QFont("MS Shell Dlg 2", 16))
       	self.canvas = FigureCanvas(Figure(figsize=(8, 5), dpi=100))
        self.toolbar = NavigationToolbar(self.canvas, self)
        

        vertical_layout = QVBoxLayout()

        vertical_layout.addWidget(self.lblTitle, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignBottom)
        vertical_layout.addWidget(self.canvas)
        #vertical_layout.addWidget(self.toolbar)
        
        self.canvas.axes = self.canvas.figure.add_subplot(111)
        #self.canvas.figure, self.canvas.axes = plt.subplots()

        self.setLayout(vertical_layout)

        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.canvas.updateGeometry()

    def display_result(self, counts):

        self.Clear()

        tab_names = ['Price', 'Scales', 'Minimum Fee']

        labels = list(counts.keys())
        data = np.array(list(counts.values()))
        data_cum = data.cumsum(axis=1)
        tab_colors = plt.get_cmap('RdYlGn')(
        np.linspace(0.15, 0.85, data.shape[1]))

        #self.canvas.figure, self.canvas.axes = plt.subplots(figsize=(9.2, 5))

        # Set Canvas figure title 
        #plt.title('Pricing Template counts per Usage Type')
        #self.canvas.figure.suptitle('Pricing Template counts per Usage Type', y=0.1, fontsize=16)

        self.canvas.axes.invert_yaxis()
        self.canvas.axes.xaxis.set_visible(False)

        self.canvas.axes.set_xlim(0, np.sum(data, axis=1).max())

        for i, (colname, color) in enumerate(zip(tab_names, tab_colors)):
            widths = data[:, i]
            starts = data_cum[:, i] - widths
            self.canvas.axes.barh(labels, widths, left=starts, height=0.5,
            					label=colname, color=color)
            xcenters = starts + widths / 2

            r, g, b, _ = color
            text_color = 'white' if r * g * b < 0.5 else 'darkgrey'

            for y, (x, c) in enumerate(zip(xcenters, widths)):
                self.canvas.axes.text(x, y, str(int(c)), ha='center', va='center',color=text_color)

    	# self.canvas.axes.legend(ncol=len(tab_names), bbox_to_anchor=(0,1,2,0.2),
    	# 						loc='lower left', borderaxespad=0, fontsize='small', mode = "expand")


        self.canvas.axes.legend(bbox_to_anchor=(0,1.02,1,0.2), loc="lower left",
                mode="expand", borderaxespad=0, fontsize='small', ncol=len(tab_names))

        #self.canvas.axes.title('Pricing Template counts per Usage Type')
        #self.canvas.axes.legend(bbox_to_anchor=(1.04,1), borderaxespad=0)
        self.canvas.figure.tight_layout()

    
    def Clear(self):
        self.canvas.axes.clear()
        #self.canvas.draw()

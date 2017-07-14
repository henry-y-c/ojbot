"""This module plot a scatter plot using pyqtgraph and OpenGL."""
from PyQt5 import QtCore, QtGui
import pyqtgraph.opengl as gl
import numpy as np

class PointCloudGraph:
    def __init__(self, buffer):
        self.buffer = buffer
        self.pos = np.empty((0,3))
        self.app = QtGui.QApplication([])
        self.win = gl.GLViewWidget()
        self.win.setWindowTitle('Test point cloud with pyqtgraph')
        self.grid = gl.GLGridItem()
        self.sp = gl.GLScatterPlotItem(pos=self.pos, color=(1,1,1,0.5), size=4, pxMode=False)
        self.win.addItem(self.grid)
        self.win.addItem(self.sp)
        self.win.show()
    
    def addData(self, pos):
        self.pos = np.append(self.pos, pos, axis=0)
        self.sp.setData(pos=self.pos)
    
    def addDataArray(self, posArray):
        for pos in posArray:
            self.pos = np.append(self.pos, pos, axis=0)
        self.sp.setData(pos=self.pos)

    def start(self):
        self.app.exec_()
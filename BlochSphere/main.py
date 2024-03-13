import subprocess
import sys
import time

import numpy as np
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QMainWindow, QVBoxLayout, QWidget, QPushButton, QMessageBox)
import server

server_start = ""


class Window(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)

        self._main = QWidget()
        self.setCentralWidget(self._main)

        self.fig = Figure()
        self.canvas = FigureCanvasQTAgg(self.fig)

        self.menu = self.menuBar()
        self.menu_base = self.menu.addMenu("Menu")
        self.menu_connect = QAction("Connect phone", self)
        self.menu_connect.triggered.connect(self.ConnectPhone)

        self.menu_base.addAction(self.menu_connect)
        self.menu.addMenu(self.menu_base)

        sphereLayout = QHBoxLayout(self._main)
        sphereLayout.addWidget(self.canvas)
        self.DrawSphere()

    def ConnectPhone(self):
        server_start = server.Server('192.168.0.105', 8888)
        msg_conn = QMessageBox()
        if server_start.hosting():
            """
            msg_conn.setText("Phone connected")
            msg_conn.exec()"""
            self.rotate(server_start)

        else:
            msg_conn.setIcon(QMessageBox.Critical)
            msg_conn.setText("Phone connection failed, check the host and port")
            msg_conn.exec()

    def DrawSphere(self):
        self._ax = self.canvas.figure.add_subplot(projection="3d")

        phi = np.linspace(0, 2 * np.pi, 25)
        theta = np.linspace(0, np.pi, 25)
        self.X = np.outer(np.cos(phi), np.sin(theta))
        self.Y = np.outer(np.sin(phi), np.sin(theta))
        self.Z = np.outer(1, np.cos(theta))

        self._ax.plot_surface(self.X, self.Y, self.Z, color='w', edgecolor='black')
        self._ax.set_aspect('equal')
        self._ax.set_axis_off()
        self.canvas.draw()

    def rotate(self,server_start):
        while True:
            angles = server_start.get_data()
            print(angles)
            """
            self._ax.view_init(int(float(angles[0])), int(float(angles[1])))
            self.fig.set_canvas(self.canvas)
            self.canvas.draw()"""


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Window()
    w.setFixedSize(500, 500)
    w.show()
    app.exec()

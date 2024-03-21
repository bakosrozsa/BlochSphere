import math
import sys
import socket
import random
import threading

import matplotlib.pyplot as plt
from PySide6.QtCore import Slot, QObject, Signal
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from PySide6.QtGui import QAction, QPixmap, Qt, QMovie
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QMainWindow, QVBoxLayout, QWidget, QMessageBox,
                               QComboBox, QTextEdit, QPushButton, QLabel)

import server
from qiskit.visualization import plot_bloch_vector

hostname = socket.gethostname()
server_start = server.Server(socket.gethostbyname(hostname), 8888)


def ConnectPhone():
    phone_connector = PhoneConnector()
    phone_connector.connected.connect(show_phone_connected_message)
    phone_thread = threading.Thread(target=phone_connector.run)
    phone_thread.start()


def show_phone_connected_message():
    msg_conn = QMessageBox()
    msg_conn.setText("Phone connected")
    msg_conn.exec()


class PhoneConnector(QObject):
    connected = Signal()

    def run(self):
        if server_start.hosting():
            self.connected.emit()


def show_message(text):
    msg_done = QMessageBox()
    msg_done.setText(text)
    msg_done.exec()


class Window(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)

        self._main = QWidget()
        self.setCentralWidget(self._main)

        self.setWindowTitle("Quantum logic gates teaching program")

        self.fig = plot_bloch_vector([1, 0, 0], coord_type='spherical')
        self.canvas = FigureCanvasQTAgg(self.fig)

        self.menu = self.menuBar()
        self.menu_states = self.menu.addMenu("States")
        self.menu_connections = self.menu.addMenu("Connection")

        self.theta, self.phi = 0.0, 0.0
        self.menu_random = QAction("Random Bloch state", self)
        self.menu_random.triggered.connect(self.RandomState)

        self.zeroState = QAction("|0> bloch state", self)
        self.zeroState.triggered.connect(self.ZeroState)

        self.oneState = QAction("|1> bloch state", self)
        self.oneState.triggered.connect(self.OneState)

        self.connected = False
        self.menu_connect = QAction("Connect phone", self)
        self.menu_connect.triggered.connect(self.ConnectPhoneThread)

        self.menu_states.addAction(self.menu_random)
        self.menu_states.addAction(self.zeroState)
        self.menu_states.addAction(self.oneState)
        self.menu_connections.addAction(self.menu_connect)
        self.menu.addMenu(self.menu_states)

        self.gatescombo = QComboBox()
        self.text = QTextEdit()
        self.gatescombo.addItems(["Identity", "Hadamard", "Pauli-X", "Pauli-Y", "Pauli-Z"])
        self.gatescombo.setCurrentIndex(-1)

        self.text.insertHtml("<h1 style='text-align: center;'>Quantum logic gates</h1>"
                             "<p style='font-size: 15px; text-align: justify;'>In quantum computing and specifically "
                             "the quantum circuit model of computation,a quantum logic gate (or simply quantum gate) "
                             "is a basic quantum circuit operating on a small number of qubits. Quantum logic gates "
                             "are the building blocks of quantum circuits, like classical logic gates are for "
                             "conventional digital circuits.</p>"
                             "<p style='font-size: 15px; text-align: justify;'>This app shows you a few quantum logic "
                             "gates, provides you small description about them. Most importantly, you can connect "
                             "your phone, and try some states by yourself (as you can see on the left side). Keep in "
                             "mind, that there are several other quantum logic gates, but these are the most common "
                             "ones.</p>")

        self.text.setReadOnly(True)
        self.label = QLabel()
        self.pixmap = QPixmap()
        self.label.setPixmap(self.pixmap)
        self.showAnim = QPushButton()
        self.startmessurebutton = QPushButton()
        self.label.setVisible(False)
        self.showAnim.setVisible(False)
        self.startmessurebutton.setVisible(False)

        self.rside = QVBoxLayout()
        self.rside.addWidget(self.gatescombo)
        self.rside.addWidget(self.text)
        self.rside.addWidget(self.label)
        self.rside.addWidget(self.showAnim)
        self.rside.addWidget(self.startmessurebutton)
        self.rside.setAlignment(self.label, Qt.AlignCenter)

        sphereLayout = QHBoxLayout(self._main)
        sphereLayout.addWidget(self.canvas)
        sphereLayout.addLayout(self.rside, 30)

        self.gatescombo.currentTextChanged.connect(self.gatescombo_options)

        self.whichGate = ""
        self.continueRotating = True
        self.showAnim.clicked.connect(self.open_another_window)
        self.startmessurebutton.clicked.connect(self.StartGateCheck)

    def open_another_window(self):
        if self.whichGate == "x":
            self.another_window = AnimationWindow("x.gif", self)
        elif self.whichGate == "y":
            self.another_window = AnimationWindow("y.gif", self)
        elif self.whichGate == "z":
            self.another_window = AnimationWindow("z.gif", self)
        elif self.whichGate == "h":
            self.another_window = AnimationWindow("h.gif", self)
        self.another_window.show()

    def RandomState(self):
        self.theta = random.uniform(0, math.pi)
        self.phi = random.uniform(0, 2 * math.pi)
        plt.close()
        self.fig.canvas.flush_events()
        self.fig = plot_bloch_vector([1, self.theta, self.phi],
                                     coord_type='spherical')
        self.canvas.figure = self.fig
        self.fig.set_canvas(self.canvas)
        self.canvas.draw()

    def ZeroState(self):
        self.theta = 0
        self.phi = 0
        plt.close()
        self.fig.canvas.flush_events()
        self.fig = plot_bloch_vector([1, self.theta, self.phi],
                                     coord_type='spherical')
        self.canvas.figure = self.fig
        self.fig.set_canvas(self.canvas)
        self.canvas.draw()

    def OneState(self):
        self.theta = math.pi
        self.phi = 0
        plt.close()
        self.fig.canvas.flush_events()
        self.fig = plot_bloch_vector([1, self.theta, self.phi],
                                     coord_type='spherical')
        self.canvas.figure = self.fig
        self.fig.set_canvas(self.canvas)
        self.canvas.draw()

    def StartGateCheck(self):
        if self.connected:
            if self.whichGate == "i":
                # nullával való szorzás?
                while self.continueRotating:
                    angles = server_start.get_data()
                    if angles is None:
                        self.connected = False
                        show_message("Phone disconnected! Please reconnect to continue!")
                        break
                    else:
                        self.rotate(angles)

            elif self.whichGate == "x":
                self.theta = math.pi - self.theta
                self.phi = -self.phi
                while self.continueRotating:
                    angles = server_start.get_data()
                    if angles is None:
                        self.connected = False
                        show_message("Phone disconnected! Please reconnect to continue!")
                        break
                    else:
                        self.rotate(angles)

            elif self.whichGate == "y":
                self.theta = math.pi - self.theta
                self.phi = math.pi - self.phi
                while self.continueRotating:
                    angles = server_start.get_data()
                    if angles is None:
                        self.connected = False
                        show_message("Phone disconnected! Please reconnect to continue!")
                        break
                    else:
                        self.rotate(angles)

            elif self.whichGate == "z":
                self.phi = math.pi + self.phi
                while self.continueRotating:
                    angles = server_start.get_data()
                    if angles is None:
                        self.connected = False
                        show_message("Phone disconnected! Please reconnect to continue!")
                        break
                    else:
                        self.rotate(angles)
            """
            elif self.whichGate == "h":
                self.rotate()
            self.continueRotating = True"""
            show_message("Done rotating!")
            self.continueRotating = True
        else:
            show_message("Connect your phone first!")

    def ConnectPhoneThread(self):
        ConnectPhone()
        self.connected = True

    def rotate(self, angles):
        try:
            plt.close()
            self.fig.canvas.flush_events()
            self.fig = plot_bloch_vector([1, float(angles[0]), float(angles[1])], coord_type='spherical')
            self.canvas.figure = self.fig
            self.fig.set_canvas(self.canvas)
            self.canvas.draw()
            if ((self.theta * 0.9 <= float(angles[0]) or -(self.theta * 0.9) >= float(angles[0])) and
                    (self.phi * 0.9 <= float(angles[1]) or -(self.phi * 0.9) >= float(angles[1]))):
                self.continueRotating = False
            else:
                self.continueRotating = True
        except ValueError:
            self.continueRotating = True

    @Slot()
    def gatescombo_options(self, text):
        self.text.clear()
        self.rside.update()
        self.showAnim.setVisible(True)
        self.startmessurebutton.setVisible(True)
        self.label.setVisible(True)
        if text == "Identity":
            self.text.setHtml("<h1 style='text-align: center;'>Identity Gate</h1>"
                              "<p style='font-size: 15px; text-align: justify;'>The Identity gate is a single-qubit "
                              "operation that leaves the basis states |0> and |1> unchanged.</p>")

            self.pixmap.load('Identity.png')
            self.whichGate = "i"
            self.showAnim.setVisible(False)
            self.startmessurebutton.setText("Try Identity gate!")
        elif text == "Hadamard":
            self.text.setHtml("<h1 style='text-align: center;'>Hadamard Gate</h1>"
                              "<p style='font-size: 15px; text-align: justify;'>This gate creates a superposition "
                              "state by transforming the |0⟩ state into an equal superposition of the |0⟩ and |1⟩ "
                              "states.</p>")

            self.pixmap.load('hadamard.png')
            self.whichGate = "h"
            self.showAnim.setText("See Hadamard gate animation!")
            self.startmessurebutton.setText("Try Hadamard gate!")
        elif text == "Pauli-X":
            self.text.setHtml("<h1 style='text-align: center;'>Pauli-X gate (or X gate)</h1>"
                              "<p style='font-size: 15px; text-align: justify;'>This gate is analogous to the NOT "
                              "gate in classical computing. It flips the state of the qubit from |0⟩ to |1⟩ or from "
                              "|1⟩ to |0⟩.</p>")
            self.pixmap.load('paulix.png')
            self.whichGate = "x"
            self.showAnim.setText("See Pauli-X gate animation!")
            self.startmessurebutton.setText("Try Pauli-X gate!")
        elif text == "Pauli-Y":
            self.text.setHtml("<h1 style='text-align: center;'>Pauli-Y gate (or Y gate)</h1> <p style='font-size: "
                              "15px; text-align: justify;'>This gate is equivalent to applying both X and Z gates and "
                              "a global phase.</p>")
            self.pixmap.load('pauliy.png')
            self.whichGate = "y"
            self.showAnim.setText("See Pauli-Y gate animation!")
            self.startmessurebutton.setText("Try Pauli-Y gate!")
        elif text == "Pauli-Z":
            self.text.setHtml("<h1 style='text-align: center;'>Pauli-Z gate (or Z gate)</h1>"
                              "<p style='font-size: 15px; text-align: justify;'>This gate flips the phase of the |1⟩ "
                              "state, leaving the |0⟩ state unchanged.</p>")
            self.pixmap.load('pauliz.png')
            self.whichGate = "z"
            self.showAnim.setText("See Pauli-Z gate animation!")
            self.startmessurebutton.setText("Try Pauli-Z gate!")
        self.label.setPixmap(self.pixmap)


class AnimationWindow(QMainWindow):
    def __init__(self, gate, parent=None):
        QMainWindow.__init__(self, parent)

        self.setWindowTitle("Gate animation")
        self.setFixedSize(500, 500)

        self.gif_label = QLabel(self)
        self.gif_label.setFixedSize(500, 500)

        self.gif_path = gate

        self.display_gif()

    def display_gif(self):
        movie = QMovie(self.gif_path)
        self.gif_label.setMovie(movie)
        movie.start()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Window()
    w.setFixedSize(1000, 500)
    w.show()
    app.exec()

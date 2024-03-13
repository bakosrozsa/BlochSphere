import asyncio
import sys
import socket

import matplotlib.pyplot as plt
from PySide6.QtCore import Slot
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from PySide6.QtGui import QAction, QPixmap, Qt
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QMainWindow, QVBoxLayout, QWidget, QMessageBox,
                               QComboBox, QTextEdit, QPushButton, QLabel)
from qiskit import QuantumCircuit

import server
from qiskit.visualization import plot_bloch_vector

hostname = socket.gethostname()
server_start = server.Server(socket.gethostbyname(hostname), 8888)


class Window(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)

        self._main = QWidget()
        self.setCentralWidget(self._main)

        self.fig = plot_bloch_vector([1, 0, 0], coord_type='spherical')
        self.canvas = FigureCanvasQTAgg(self.fig)

        self.menu = self.menuBar()
        self.menu_base = self.menu.addMenu("Menu")
        self.menu_connect = QAction("Connect phone", self)
        self.menu_connect.triggered.connect(self.ConnectPhone)

        self.menu_base.addAction(self.menu_connect)
        self.menu.addMenu(self.menu_base)

        self.gatescombo = QComboBox()
        self.text = QTextEdit()
        self.gatescombo.addItems(["Hadamard", "Pauli-X", "Pauli-Y", "Pauli-Z"])
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
        self.startmessurebutton = QPushButton()
        self.label.setVisible(False)
        self.startmessurebutton.setVisible(False)

        self.rside = QVBoxLayout()
        self.rside.addWidget(self.gatescombo)
        self.rside.addWidget(self.text)
        self.rside.addWidget(self.label)
        self.rside.addWidget(self.startmessurebutton)
        self.rside.setAlignment(self.label, Qt.AlignCenter)

        sphereLayout = QHBoxLayout(self._main)
        sphereLayout.addWidget(self.canvas)
        sphereLayout.addLayout(self.rside, 30)

        self.gatescombo.currentTextChanged.connect(self.gatescombo_options)
        self.startmessurebutton.clicked.connect(self.StartGateCheck)

    def StartGateCheck(self):
        asyncio.run(self.rotate())
        server_start.conn.close()

    def ConnectPhone(self):

        msg_conn = QMessageBox()
        if server_start.hosting():

            msg_conn.setText("Phone connected")
            msg_conn.exec()

        else:
            msg_conn.setIcon(QMessageBox.Critical)
            msg_conn.setText("Phone connection failed, check the host and port")
            msg_conn.exec()

    async def rotate(self):
        angles = server_start.get_data()
        while True:
            #plt.close()
            #self.fig.canvas.flush_events()
            print(angles)
            #self.fig = plot_bloch_vector([1, float(angles[0]), float(angles[1])], coord_type='spherical')
            #self.canvas.figure = self.fig
            #self.fig.set_canvas(self.canvas)
            #self.canvas.draw()
            angles = server_start.get_data()

    @Slot()
    def gatescombo_options(self, text):
        self.text.clear()
        self.rside.update()
        self.startmessurebutton.setVisible(True)
        self.label.setVisible(True)
        circuit = QuantumCircuit(1)
        if text == "Hadamard":
            self.text.setHtml("<h1 style='text-align: center;'>Hadamard Gate</h1>"
                              "<p style='font-size: 15px; text-align: justify;'>This gate creates a superposition "
                              "state by transforming the |0⟩ state into an equal superposition of the |0⟩ and |1⟩ "
                              "states.</p>")

            circuit.h(0)
            circuit.draw(output="mpl", filename='hadamard.png')
            self.pixmap.load('hadamard.png')
            self.startmessurebutton.setText("Try Hadamard gate!")
        elif text == "Pauli-X":
            self.text.setHtml("<h1 style='text-align: center;'>Pauli-X gate (or X gate)</h1>"
                              "<p style='font-size: 15px; text-align: justify;'>This gate is analogous to the NOT "
                              "gate in classical computing. It flips the state of the qubit from |0⟩ to |1⟩ or from "
                              "|1⟩ to |0⟩.</p>")
            circuit.x(0)
            circuit.draw(output="mpl", filename='paulix.png')
            self.pixmap.load('paulix.png')
            self.startmessurebutton.setText("Try Pauli-X gate!")
        elif text == "Pauli-Y":
            self.text.setHtml("<h1 style='text-align: center;'>Pauli-Y gate (or Y gate)</h1> <p style='font-size: "
                              "15px; text-align: justify;'>This gate is equivalent to applying both X and Z gates and "
                              "a global phase.</p>")
            circuit.y(0)
            circuit.draw(output="mpl", filename='pauliy.png')
            self.pixmap.load('pauliy.png')
            self.startmessurebutton.setText("Try Pauli-Y gate!")
        elif text == "Pauli-Z":
            self.text.setHtml("<h1 style='text-align: center;'>Pauli-Z gate (or Z gate)</h1>"
                              "<p style='font-size: 15px; text-align: justify;'>This gate flips the phase of the |1⟩ "
                              "state, leaving the |0⟩ state unchanged.</p>")
            circuit.z(0)
            circuit.draw(output="mpl", filename='pauliz.png')
            self.pixmap.load('pauliz.png')
            self.startmessurebutton.setText("Try Pauli-Z gate!")
        self.label.setPixmap(self.pixmap)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Window()
    w.setFixedSize(1000, 500)
    w.show()
    app.exec()

import math
import random
import socket
import sys
import threading

import matplotlib.pyplot as plt
import numpy as np
from PySide6.QtCore import Slot, QObject, Signal
from PySide6.QtGui import QAction, QPixmap, Qt
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QMainWindow, QVBoxLayout, QWidget, QMessageBox,
                               QComboBox, QTextEdit, QPushButton, QLabel)
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from qiskit.visualization import plot_bloch_vector

import AnimWindow
import server
import BlochVector

hostname = socket.gethostname()
server_start = server.Server(socket.gethostbyname(hostname), 0)


def connect_phone():
    phone_connector = PhoneConnector()
    phone_connector.connected.connect(show_phone_connected_message)
    phone_thread = threading.Thread(target=phone_connector.run)
    phone_thread.start()


class PhoneConnector(QObject):
    connected = Signal()

    def run(self):
        if server_start.hosting():
            self.connected.emit()


def show_phone_connected_message():
    msg_conn = QMessageBox()
    msg_conn.setText("Phone connected")
    msg_conn.exec()


def show_message(text):
    msg_done = QMessageBox()
    msg_done.setText(text)
    msg_done.exec()


class Window(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)

        self._main = QWidget()

        # Menu Bar
        self.menu = self.menuBar()
        self.menu_states = self.menu.addMenu("States")
        self.menu_random = QAction("Random Bloch state", self)
        self.zero_state_option = QAction("|0> bloch state", self)
        self.one_state_option = QAction("|1> bloch state", self)

        # Bloch sphere part
        self.bloch_vector = BlochVector.BlochVector(0.0, 0.0)
        self.fig = plot_bloch_vector([1, self.bloch_vector.theta, self.bloch_vector.phi], coord_type='spherical')
        self.canvas = FigureCanvasQTAgg(self.fig)

        # Right side of the program
        self.addr_label = QLabel()
        self.gates_combo = QComboBox()
        self.info_text = QTextEdit()
        self.label = QLabel()
        self.pixmap = QPixmap()
        self.show_anim = QPushButton()
        self.start_measure_button = QPushButton()
        self.coordinate_label = QLabel()
        self.current_coordinate_label = QLabel()
        self.right_side = QVBoxLayout()
        self.which_gate = ""

        # Set UI elements
        self.__start_program()

    def __start_program(self):
        self.setWindowTitle("Quantum logic gates teaching program")

        self.setCentralWidget(self._main)

        # Menu Bar
        self.menu_random.triggered.connect(self.__random_state)
        self.zero_state_option.triggered.connect(self.__zero_state)
        self.one_state_option.triggered.connect(self.__one_state)
        self.menu_states.addAction(self.menu_random)
        self.menu_states.addAction(self.zero_state_option)
        self.menu_states.addAction(self.one_state_option)
        self.menu.addMenu(self.menu_states)

        # Bloch sphere part
        sphere_layout = QHBoxLayout(self._main)
        sphere_layout.addWidget(self.canvas)
        sphere_layout.addLayout(self.right_side, 30)

        # Right side of the program
        self.addr_label.setText("Server address for phone: " + str(server_start.host) + ":" + str(server_start.port))

        self.gates_combo.addItems(["Home", "Identity", "Pauli-X", "Pauli-Y", "Pauli-Z", "Hadamard", "Phase", "T"])

        self.label.setPixmap(self.pixmap)

        self.coordinate_label.setText("You will see the required sphere coordinates here")
        self.current_coordinate_label.setText("\u03F4: " + str(self.bloch_vector.theta)
                                              + "\t\u03A6: " + str(self.bloch_vector.phi))

        self.info_text.setReadOnly(True)
        self.label.setVisible(False)
        self.show_anim.setVisible(False)
        self.start_measure_button.setVisible(False)

        self.right_side.addWidget(self.addr_label)
        self.right_side.addWidget(self.gates_combo)
        self.right_side.addWidget(self.info_text)
        self.right_side.addWidget(self.label)
        self.right_side.addWidget(self.show_anim)
        self.right_side.addWidget(self.start_measure_button)
        self.right_side.addWidget(self.coordinate_label)
        self.right_side.addWidget(self.current_coordinate_label)
        self.right_side.setAlignment(self.addr_label, Qt.AlignCenter)
        self.right_side.setAlignment(self.label, Qt.AlignCenter)
        self.right_side.setAlignment(self.coordinate_label, Qt.AlignCenter)
        self.right_side.setAlignment(self.current_coordinate_label, Qt.AlignCenter)

        self.gates_combo.currentTextChanged.connect(self.gates_combo_options)
        self.show_anim.clicked.connect(self.__open_anim_window)
        self.start_measure_button.clicked.connect(self.__start_gate_check)

    def __random_state(self):
        # Set Bloch sphere to a random state
        self.bloch_vector.theta = random.uniform(0.0, np.pi)
        self.bloch_vector.phi = random.uniform(0.0, 2 * np.pi)
        plt.close()
        self.fig.canvas.flush_events()
        self.fig = plot_bloch_vector([1, self.bloch_vector.theta, self.bloch_vector.phi],
                                     coord_type='spherical')
        self.canvas.figure = self.fig
        self.fig.set_canvas(self.canvas)
        self.canvas.draw()
        self.current_coordinate_label.setText("\u03F4: " + str(self.bloch_vector.theta)
                                              + "\t\u03A6: " + str(self.bloch_vector.phi))

    def __zero_state(self):
        # Set Bloch sphere to the zero state
        self.bloch_vector.theta = 0.0
        self.bloch_vector.phi = 0.0
        plt.close()
        self.fig.canvas.flush_events()
        self.fig = plot_bloch_vector([1, self.bloch_vector.theta, self.bloch_vector.phi],
                                     coord_type='spherical')
        self.canvas.figure = self.fig
        self.fig.set_canvas(self.canvas)
        self.canvas.draw()
        self.current_coordinate_label.setText("\u03F4: " + str(self.bloch_vector.theta)
                                              + "\t\u03A6: " + str(self.bloch_vector.phi))

    def __one_state(self):
        # Set Bloch sphere to the one state
        self.bloch_vector.theta = np.pi
        self.bloch_vector.phi = 0.0
        plt.close()
        self.fig.canvas.flush_events()
        self.fig = plot_bloch_vector([1, self.bloch_vector.theta, self.bloch_vector.phi],
                                     coord_type='spherical')
        self.canvas.figure = self.fig
        self.fig.set_canvas(self.canvas)
        self.canvas.draw()
        self.current_coordinate_label.setText("\u03F4: " + str(self.bloch_vector.theta)
                                              + "\t\u03A6: " + str(self.bloch_vector.phi))

    @Slot()
    def gates_combo_options(self, text):
        self.info_text.clear()
        self.right_side.update()
        self.show_anim.setVisible(True)
        self.start_measure_button.setVisible(True)
        self.label.setVisible(True)
        if text == "Home":
            self.info_text.insertHtml("<h1 style='text-align: center;'>Quantum logic gates</h1>"
                                      "<p style='font-size: 15px; text-align: justify;'>In quantum computing and "
                                      "specifically "
                                      "the quantum circuit model of computation,a quantum logic gate (or simply "
                                      "quantum gate)"
                                      "is a basic quantum circuit operating on a small number of qubits. Quantum "
                                      "logic gates "
                                      "are the building blocks of quantum circuits, like classical logic gates are for "
                                      "conventional digital circuits.</p>"
                                      "<p style='font-size: 15px; text-align: justify;'>This app shows you a few "
                                      "quantum logic "
                                      "gates, provides you small description about them. Most importantly, you can "
                                      "connect "
                                      "your phone, and try some states by yourself (as you can see on the left side). "
                                      "Keep in "
                                      "mind, that there are several other quantum logic gates, but these are the most "
                                      "common ones that are using one qubit.</p>")
            self.show_anim.setVisible(False)
            self.start_measure_button.setVisible(False)
            self.label.setVisible(False)

        if text == "Identity":
            self.info_text.setHtml("<h1 style='text-align: center;'>Identity Gate</h1>"
                                   "<p style='font-size: 15px; text-align: justify;'>The Identity gate is a "
                                   "single-qubit "
                                   "operation that leaves the basis states |0> and |1> unchanged.</p>")

            self.pixmap.load('images/Identity.png')
            self.which_gate = "i"
            self.show_anim.setVisible(False)
            self.start_measure_button.setText("Try Identity gate!")
        elif text == "Pauli-X":
            self.info_text.setHtml("<h1 style='text-align: center;'>Pauli-X gate (or X gate)</h1>"
                                   "<p style='font-size: 15px; text-align: justify;'>This gate is analogous to "
                                   "the NOT "
                                   "gate in classical computing. It flips the state of the qubit from |0⟩ to |1⟩ or "
                                   "from"
                                   "|1⟩ to |0⟩.</p>")
            self.pixmap.load('images/paulix.png')
            self.which_gate = "x"
            self.show_anim.setText("See Pauli-X gate animation!")
            self.start_measure_button.setText("Try Pauli-X gate!")
        elif text == "Pauli-Y":
            self.info_text.setHtml(
                "<h1 style='text-align: center;'>Pauli-Y gate (or Y gate)</h1> <p style='font-size: "
                "15px; text-align: justify;'>This gate is equivalent to applying both X and Z gates and "
                "a global phase.</p>")
            self.pixmap.load('images/pauliy.png')
            self.which_gate = "y"
            self.show_anim.setText("See Pauli-Y gate animation!")
            self.start_measure_button.setText("Try Pauli-Y gate!")
        elif text == "Pauli-Z":
            self.info_text.setHtml("<h1 style='text-align: center;'>Pauli-Z gate (or Z gate)</h1>"
                                   "<p style='font-size: 15px; text-align: justify;'>This gate flips the phase "
                                   "of the |1⟩"
                                   "state, leaving the |0⟩ state unchanged.</p>")
            self.pixmap.load('images/pauliz.png')
            self.which_gate = "z"
            self.show_anim.setText("See Pauli-Z gate animation!")
            self.start_measure_button.setText("Try Pauli-Z gate!")
        elif text == "Hadamard":
            self.info_text.setHtml("<h1 style='text-align: center;'>Hadamard Gate</h1>"
                                   "<p style='font-size: 15px; text-align: justify;'>This gate creates a "
                                   "superposition "
                                   "state by transforming the |0⟩ state into an equal superposition of the |0⟩ and |1⟩ "
                                   "states.</p>")

            self.pixmap.load('images/hadamard.png')
            self.which_gate = "h"
            self.show_anim.setText("See Hadamard gate animation!")
            self.start_measure_button.setText("Try Hadamard gate!")
        elif text == "Phase":
            self.info_text.setHtml("<h1 style='text-align: center;'>Phase Gate (or S gate)</h1>"
                                   "<p style='font-size: 15px; text-align: justify;'>The S gate is also known as "
                                   "the phase "
                                   "gate or the Z90 gate, because it represents a 90-degree rotation around the "
                                   "z-axis.</p>")

            self.pixmap.load('images/phase.png')
            self.which_gate = "s"
            self.show_anim.setText("See Phase gate animation!")
            self.start_measure_button.setText("Try Phase gate!")
        elif text == "T":
            self.info_text.setHtml("<h1 style='text-align: center;'>T Gate</h1>"
                                   "<p style='font-size: 15px; text-align: justify;'>It induces a π/4 phase, "
                                   "and is sometimes called the pi/8 gate</p>")

            self.pixmap.load('images/tGate.png')
            self.which_gate = "t"
            self.show_anim.setText("See T gate animation!")
            self.start_measure_button.setText("Try T gate!")
        self.label.setPixmap(self.pixmap)

    def __open_anim_window(self):
        if self.which_gate == "x":
            anim_window = AnimWindow.AnimationWindow("images/x.gif", self)
        elif self.which_gate == "y":
            anim_window = AnimWindow.AnimationWindow("images/y.gif", self)
        elif self.which_gate == "z":
            anim_window = AnimWindow.AnimationWindow("images/z.gif", self)
        elif self.which_gate == "h":
            anim_window = AnimWindow.AnimationWindow("images/h.gif", self)
        elif self.which_gate == "s":
            anim_window = AnimWindow.AnimationWindow("images/s.gif", self)
        elif self.which_gate == "t":
            anim_window = AnimWindow.AnimationWindow("images/t.gif", self)
        anim_window.show()

    def __start_gate_check(self):
        # Apply gate on Bloch sphere and then start the checking
        self.start_measure_button.setEnabled(False)
        try:
            if self.which_gate == "i":
                self.bloch_vector.identity()

            elif self.which_gate == "x":
                self.bloch_vector.pauli_x()

            elif self.which_gate == "y":
                self.bloch_vector.pauli_y()

            elif self.which_gate == "z":
                self.bloch_vector.pauli_z()

            elif self.which_gate == "h":
                self.bloch_vector.hadamard()

            elif self.which_gate == "s":
                self.bloch_vector.phase()

            elif self.which_gate == "t":
                self.bloch_vector.t()
            self.__rotate()
        except OSError:
            self.coordinate_label.setText("You will see the required sphere coordinates here")
            self.__zero_state()
            show_message("Connect your phone first")
        except AttributeError:
            self.coordinate_label.setText("You will see the required sphere coordinates here")
            self.__zero_state()
            show_message("Connect your phone first")
        self.start_measure_button.setEnabled(True)

    def __rotate(self):
        # Start rotating and checking
        self.coordinate_label.setText("\u03F4: " + str(self.bloch_vector.theta) +
                                      "\t\u03A6: " + str(self.bloch_vector.phi))
        while True:
            angles = server_start.get_data()
            if angles is None:
                show_message("Phone disconnected! Please reconnect to continue!")
                self.__zero_state()
                connect_phone()
                break
            else:
                try:
                    angles = np.array(angles, dtype=float)
                    if angles[1] < 0:
                        angles[1] = angles[1] + 2 * np.pi
                    self.current_coordinate_label.setText("\u03F4: " + str(angles[0])
                                                          + "\t\u03A6: " + str(angles[1]))
                    plt.close()
                    self.fig.canvas.flush_events()
                    self.fig = plot_bloch_vector([1, angles[0], angles[1]], coord_type='spherical')
                    self.canvas.figure = self.fig
                    self.fig.set_canvas(self.canvas)
                    self.canvas.draw()
                except ValueError:
                    continue
                if (math.isclose(self.bloch_vector.theta, angles[0], rel_tol=0.1, abs_tol=0.15) and
                        math.isclose(self.bloch_vector.phi, angles[1], rel_tol=0.1, abs_tol=0.15)):
                    show_message("Done rotating!")
                    break


if __name__ == "__main__":
    connect_phone()
    app = QApplication(sys.argv)
    w = Window()
    w.setFixedSize(1000, 500)
    w.gates_combo_options("Home")
    w.show()
    app.exec()

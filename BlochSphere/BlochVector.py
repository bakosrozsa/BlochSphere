import numpy as np


class BlochVector:
    def __init__(self, theta, phi):
        self.theta = theta
        self.phi = phi

    def start_state_vector(self):
        alpha = np.cos(self.theta / 2)
        beta = np.exp(1j * self.phi) * np.sin(self.theta / 2)
        state_vector = np.array([[alpha], [beta]])
        return state_vector

    def identity(self):
        identity_matrix = np.array([[1, 0], [0, 1]])
        state_vector_after_gate = np.dot(self.start_state_vector().T, identity_matrix)
        self.theta = 2 * np.arccos(state_vector_after_gate[0][0].real)
        print(self.theta)

    def pauli_x(self):
        pauli_x_matrix = np.array([[0, 1], [1, 0]])
        state_vector_after_gate = np.dot(self.start_state_vector().T, pauli_x_matrix)
        self.theta = 2 * np.arccos(state_vector_after_gate[0][0].real)
        print(self.theta)

    def pauli_y(self):
        pauli_y_matrix = np.array([[0, -1j], [1j, 0]])
        state_vector_after_gate = np.dot(self.start_state_vector().T, pauli_y_matrix)
        self.theta = 2 * np.arccos(state_vector_after_gate[0][0].real)
        print(self.theta)

    def pauli_z(self):
        pauli_z_matrix = np.array([[1, 0], [0, -1]])
        state_vector_after_gate = np.dot(self.start_state_vector().T, pauli_z_matrix)
        self.theta = 2 * np.arccos(state_vector_after_gate[0][0].real)
        print(self.theta)

    def hadamard(self):
        hadamard_matrix = (1 / np.sqrt(2)) * np.array([[1, 1], [1, -1]])
        state_vector_after_gate = np.dot(self.start_state_vector().T, hadamard_matrix)
        self.theta = 2 * np.arccos(state_vector_after_gate[0][0].real)
        print(self.theta)

    def phase(self):
        phase_matrix = np.array([[1, 0], [0, 1j]])
        state_vector_after_gate = np.dot(self.start_state_vector().T, phase_matrix)
        self.theta = 2 * np.arccos(state_vector_after_gate[0][0].real)
        print(self.theta)

    def t(self):
        t_matrix = np.array([[1, 0], [0, np.exp(1j * np.pi / 4)]])
        state_vector_after_gate = np.dot(self.start_state_vector().T, t_matrix)
        self.theta = 2 * np.arccos(state_vector_after_gate[0][0].real)
        print(self.theta)

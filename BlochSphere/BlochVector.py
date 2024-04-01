import numpy as np


def get_spherical_coordinates_from_state_vector(state_vector_after_gate):
    alpha_real = state_vector_after_gate[0][0].real
    alpha_imag = state_vector_after_gate[0][0].imag
    beta_real = state_vector_after_gate[0][1].real
    beta_imag = state_vector_after_gate[0][1].imag

    if alpha_real != 0.0:
        if alpha_real < 0 < alpha_imag:
            alpha_theta = np.arctan(alpha_imag / alpha_real) + np.pi

        elif alpha_real < 0 and alpha_imag < 0:
            alpha_theta = np.arctan(alpha_imag / alpha_real) + np.pi
        else:
            alpha_theta = np.arctan(alpha_imag / alpha_real)
    else:
        alpha_theta = 0.0

    r_alpha = np.sqrt((alpha_real ** 2) + (alpha_imag ** 2))

    if beta_real != 0.0:
        if beta_real < 0 < beta_imag:
            beta_theta = np.arctan(beta_imag / beta_real) + np.pi

        elif beta_real < 0 and beta_imag < 0:
            beta_theta = np.arctan(beta_imag / beta_real) + np.pi
        else:
            beta_theta = np.arctan(beta_imag / beta_real)
    else:
        beta_theta = 0.0

    theta = 2 * np.arccos(r_alpha)
    phi = beta_theta - alpha_theta
    coordinates = [theta, phi]
    return coordinates


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
        print(self.theta, self.phi)
        coordinates = get_spherical_coordinates_from_state_vector(state_vector_after_gate)
        self.theta = coordinates[0]
        self.phi = coordinates[1]
        print(self.theta, self.phi)

    def pauli_x(self):
        pauli_x_matrix = np.array([[0, 1], [1, 0]])
        state_vector_after_gate = np.dot(self.start_state_vector().T, pauli_x_matrix)
        coordinates = get_spherical_coordinates_from_state_vector(state_vector_after_gate)
        self.theta = coordinates[0]
        self.phi = coordinates[1]
        print(self.theta, self.phi)

    def pauli_y(self):
        pauli_y_matrix = np.array([[0, -1j], [1j, 0]])
        state_vector_after_gate = np.dot(self.start_state_vector().T, pauli_y_matrix)
        coordinates = get_spherical_coordinates_from_state_vector(state_vector_after_gate)
        self.theta = coordinates[0]
        self.phi = coordinates[1]
        print(self.theta, self.phi)

    def pauli_z(self):
        pauli_z_matrix = np.array([[1, 0], [0, -1]])
        state_vector_after_gate = np.dot(self.start_state_vector().T, pauli_z_matrix)
        coordinates = get_spherical_coordinates_from_state_vector(state_vector_after_gate)
        self.theta = coordinates[0]
        self.phi = coordinates[1]
        print(self.theta, self.phi)

    def hadamard(self):
        hadamard_matrix = (1 / np.sqrt(2)) * np.array([[1, 1], [1, -1]])
        state_vector_after_gate = np.dot(self.start_state_vector().T, hadamard_matrix)
        coordinates = get_spherical_coordinates_from_state_vector(state_vector_after_gate)
        self.theta = coordinates[0]
        self.phi = coordinates[1]
        print(self.theta, self.phi)

    def phase(self):
        phase_matrix = np.array([[1, 0], [0, 1j]])
        state_vector_after_gate = np.dot(self.start_state_vector().T, phase_matrix)
        coordinates = get_spherical_coordinates_from_state_vector(state_vector_after_gate)
        self.theta = coordinates[0]
        self.phi = coordinates[1]
        print(self.theta, self.phi)

    def t(self):
        t_matrix = np.array([[1, 0], [0, np.exp(1j * np.pi / 4)]])
        state_vector_after_gate = np.dot(self.start_state_vector().T, t_matrix)
        coordinates = get_spherical_coordinates_from_state_vector(state_vector_after_gate)
        self.theta = coordinates[0]
        self.phi = coordinates[1]
        print(self.theta, self.phi)

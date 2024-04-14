import socket
import unittest
import random
from unittest.mock import patch, MagicMock

import numpy as np

from App.main import BlochVector
from App.server import Server


class TestQuantumLogicGates(unittest.TestCase):

    def setUp(self):
        self.bloch_vector = BlochVector.BlochVector(0.0, 0.0)
        self.bloch_vector.theta = random.uniform(0.0, np.pi)
        self.bloch_vector.phi = random.uniform(0.0, 2 * np.pi)

    def test_identity_gate(self):
        original_theta = self.bloch_vector.theta
        original_phi = self.bloch_vector.phi
        self.bloch_vector.identity()
        self.assertAlmostEqual(original_theta, self.bloch_vector.theta)
        self.assertAlmostEqual(original_phi, self.bloch_vector.phi)

    def test_x_gate(self):
        original_theta = self.bloch_vector.theta
        original_phi = self.bloch_vector.phi
        self.bloch_vector.pauli_x()
        self.bloch_vector.pauli_x()
        self.assertAlmostEqual(original_theta, self.bloch_vector.theta)
        self.assertAlmostEqual(original_phi, self.bloch_vector.phi)

    def test_y_gate(self):
        original_theta = self.bloch_vector.theta
        original_phi = self.bloch_vector.phi
        self.bloch_vector.pauli_y()
        self.bloch_vector.pauli_y()
        self.assertAlmostEqual(original_theta, self.bloch_vector.theta)
        self.assertAlmostEqual(original_phi, self.bloch_vector.phi)

    def test_z_gate(self):
        original_theta = self.bloch_vector.theta
        original_phi = self.bloch_vector.phi
        self.bloch_vector.pauli_z()
        self.bloch_vector.pauli_z()
        self.assertAlmostEqual(original_theta, self.bloch_vector.theta)
        self.assertAlmostEqual(original_phi, self.bloch_vector.phi)

    def test_hadamard_gate(self):
        original_theta = self.bloch_vector.theta
        original_phi = self.bloch_vector.phi
        self.bloch_vector.hadamard()
        self.bloch_vector.hadamard()
        self.assertAlmostEqual(original_theta, self.bloch_vector.theta)
        self.assertAlmostEqual(original_phi, self.bloch_vector.phi)

    def test_phase_gate(self):
        original_theta = self.bloch_vector.theta
        original_phi = self.bloch_vector.phi
        for i in range(4):
            self.bloch_vector.phase()
        self.assertAlmostEqual(original_theta, self.bloch_vector.theta)
        self.assertAlmostEqual(original_phi, self.bloch_vector.phi)

    def test_t_gate(self):
        original_theta = self.bloch_vector.theta
        original_phi = self.bloch_vector.phi
        for i in range(8):
            self.bloch_vector.t()
        self.assertAlmostEqual(original_theta, self.bloch_vector.theta)
        self.assertAlmostEqual(original_phi, self.bloch_vector.phi)


class TestServer(unittest.TestCase):
    def test_server_binding(self):
        HOST = '127.0.0.1'
        PORT = 12345

        # Mocking the socket object
        with patch('socket.socket') as mock_socket:
            server = Server(HOST, PORT)

            # Assert that the socket was called with the correct arguments
            mock_socket.assert_called_once_with(socket.AF_INET, socket.SOCK_STREAM)

            # Mock the bind method of the socket object
            mock_socket_instance = mock_socket.return_value
            mock_socket_instance.bind.assert_called_once_with((HOST, PORT))

            # Mock the listen method of the socket object
            mock_socket_instance.listen.return_value = None

            # Mock the accept method to return a dummy connection
            dummy_conn = MagicMock()
            dummy_addr = ('127.0.0.1', 12345)
            mock_socket_instance.accept.return_value = (dummy_conn, dummy_addr)

            # Test the hosting method
            self.assertTrue(server.hosting())


if __name__ == '__main__':
    unittest.main()

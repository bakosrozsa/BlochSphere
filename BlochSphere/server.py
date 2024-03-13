import socket
import sys


class Server:
    def __init__(self, HOST, PORT):
        self.host = HOST
        self.port = PORT
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn = ""
        self.addr = ""

    def hosting(self):
        try:
            self.s.bind((self.host, self.port))
        except socket.error as error:
            return False

        self.s.listen(1)
        print('Listening...')

        self.conn, self.addr = self.s.accept()
        print('Connect with ' + self.addr[0] + ":" + str(self.addr[1]))

        return True

    def get_data(self):
        data = self.conn.recv(1024).decode()
        angles = data.split(',')
        print(angles)
        return angles
        #self.conn.close()

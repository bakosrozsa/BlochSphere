import socket


class Server:
    def __init__(self, HOST, PORT):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = HOST
        self.port = PORT
        self.s.bind((self.host, self.port))
        self.port = self.s.getsockname()[1]
        self.conn = ""
        self.addr = ""

    def hosting(self):
        self.s.listen(0)
        self.conn, self.addr = self.s.accept()
        return True

    def get_data(self):
        data = self.conn.recv(1024).decode()
        if not data:
            self.conn.close()
            return None
        else:
            angles = data.split(',')
            return angles

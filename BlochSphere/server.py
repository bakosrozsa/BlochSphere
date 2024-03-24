import socket


class Server:
    def __init__(self, HOST, PORT):
        self.host = HOST
        self.port = PORT
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((self.host, self.port))
        self.conn = ""
        self.addr = ""

    def hosting(self):
        self.s.listen(1)
        print('Listening...')
        self.conn, self.addr = self.s.accept()
        print('Connect with ' + self.addr[0] + ":" + str(self.addr[1]))
        return True

    def get_data(self):
        data = self.conn.recv(1024).decode()
        if not data:
            self.conn.close()
            return None
        else:
            angles = data.split(',')
            return angles

import socket



class UdpClient(object):

    def __init__(self, host, port=3123):
        self.host = host
        self.port = port
        self.socket = None

    def open(self):
        if not getattr(self, 'socket', None):
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def sendto(self, msg):
        self.open()
        self.socket.sendto(msg, (self.host, self.port))



if __name__ == '__main__':
    clnt = UdpClient("localhost")
    clnt.sendto("hio")


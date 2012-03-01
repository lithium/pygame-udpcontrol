


import socket



class UdpListenServer(object):

    def __init__(self, listen_ip='0.0.0.0', listen_port=3123, buffer_size=1024):
        self.listen_ip = listen_ip
        self.listen_port = listen_port
        self.buffer_size = buffer_size
        self.socket = None

    def bind(self):
        if not getattr(self, 'socket', None):
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.socket.bind((self.listen_ip, self.listen_port))

    def loop(self):
        self.bind()
        self.running = True
        while self.running:
            data, addr = self.socket.recvfrom(self.buffer_size)
            print("read data from (%s):\n%s" % (addr, data))




if __name__ == '__main__':
    srv = UdpListenServer()
    srv.loop()


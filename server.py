


import socket
import pickle
import subprocess



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
            msg = pickle.loads(data)
            print("read data from (%s):   %s" % (addr, msg))
            button = msg.get('button', None)
            if button == 'UP':
                self.tilt_up()
            elif button == 'DOWN':
                self.tilt_down()
            elif button == 'LEFT':
                self.pan_left()
            elif button == 'RIGHT':
                self.pan_right()

    def pan_left(self, v=300):
        subprocess.call(["uvcdynctrl", "-s", 'Pan (relative)', str(v)])

    def pan_right(self, v=300):
        subprocess.call(["uvcdynctrl", "-s", 'Pan (relative)', str(v*-1)])

    def tilt_up(self, v=300):
        subprocess.call(["uvcdynctrl", "-s", 'Tilt (relative)', str(v)])

    def tilt_down(self, v=300):
        subprocess.call(["uvcdynctrl", "-s", 'Tilt (relative)', str(v*-1)])




if __name__ == '__main__':
    srv = UdpListenServer()
    srv.loop()


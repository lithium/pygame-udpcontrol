import socket
import pygame
import sys
import pickle
import time

import pprint



class UdpClient(object):

    def __init__(self, host, port=3123, joystick_number=0):
        self.host = host
        self.port = port
        self.socket = None
        self.joy_number = joystick_number
        self.buttons = {
            'U': {'state': 0, 'name': 'UP'},
            'D': {'state': 0, 'name': 'DOWN'},
            'L': {'state': 0, 'name': 'LEFT'},
            'R': {'state': 0, 'name': 'RIGHT'},
            0: {'state': 0, 'name': 'A'},
            1: {'state': 0, 'name': 'B'},
            9: {'state': 0, 'name': 'START'},
            8: {'state': 0, 'name': 'SELECT'},
        }
        self.debounce = {}

    def open(self):
        if not getattr(self, 'socket', None):
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def sendto(self, **kwargs):
        self.open()
        msg = pickle.dumps(kwargs)
        self.socket.sendto(msg, (self.host, self.port))


    def _key_down(self, key, debounce=0.5):
        now = time.time()
        last = self.debounce.get(key, 0)
        if now - last > debounce:
            self.sendto(button=self.buttons[key]['name'])
            self.debounce[key] = now

    def _key_up(self, key):
        self.debounce[key] = 0


    def loop(self):
        pygame.init()
        self.joystick = pygame.joystick.Joystick(self.joy_number)
        self.joystick.init();
        self.running = True
        try:
            while self.running:
                pygame.event.pump()
                for i in range(0, self.joystick.get_numaxes()):
                    val = self.joystick.get_axis(i)
                    if val:
                        if i:
                            if val < 0:
                                but = 'U'
                            else:
                                but = 'D'
                        else:
                            if val < 0:
                                but = 'L'
                            else:
                                but = 'R'
                        self._key_down(but)

                for i in range(0, self.joystick.get_numbuttons()):
                    if i in self.buttons:
                        if self.joystick.get_button(i):
                            self._key_down(i)
                        else:
                            self._key_up(i)
        except KeyboardInterrupt as e:
            self.joystick.quit()
            



if __name__ == '__main__':
    if len(sys.argv) > 1:
        host = sys.argv[1]
    else:
        sys.stderr.write("Usage: %s <hostname> [port]\n" % (sys.argv[0]))
        sys.exit(1)

    clnt = UdpClient(host)
    clnt.loop()

# -*- coding: utf-8 -*-
__author__ = 'goms'

import asyncore, socket
import string, random
import struct

def str_generator():
    return "ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZ_"


class EchoClient(asyncore.dispatcher):

    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect( (host, port) )
        self.seq = 1
        self.buffer = str_generator()

    def handle_connect(self):
        pass
  
    def handle_close(self):
        self.close()

    def handle_read(self):
        print "[RECV]", self.recv(8192)
        self.seq += 1
        self.buffer = str_generator()

    def writable(self):
        return (len(self.buffer) > 0)

    def handle_write(self):
		sent = self.send(self.buffer)
		self.buffer = self.buffer[sent:]
		

client = EchoClient('10.73.44.30', 9002)
#client = EchoClient('10.73.44.31', 9003)
asyncore.loop()

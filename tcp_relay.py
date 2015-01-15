# -*- coding: utf-8 -*-
__author__ = 'sm9'

import asyncore, socket

CLIENT_SOCKS = []
CLIENT_NUM = 0

def relay(sock, message):
    try:
        sock.sendall(message)
    except:
        sock.close()
        CLIENT_SOCKS.remove(sock)

class MyHandler(asyncore.dispatcher_with_send):
	def __init__(self, sock, clientNum):
		asyncore.dispatcher_with_send.__init__(self, sock)
		self.targetClientNum = 1 - clientNum % 2

	def handle_read(self):
		data = self.recv(8192)
		if data:
			relay(CLIENT_SOCKS[self.targetClientNum], data)

class RelayServer(asyncore.dispatcher):

    def __init__(self, host, port):
		asyncore.dispatcher.__init__(self)
		self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
		self.set_reuse_addr()
		self.bind((host, port))
		self.listen(2)

    def handle_accept(self):
		global CLIENT_NUM
		pair = self.accept()
		print 'HELLO'
		if pair is not None:
			sock, addr = pair
			CLIENT_SOCKS.append(sock)
			print 'connected'
			handler = MyHandler(sock, CLIENT_NUM)
			CLIENT_NUM = CLIENT_NUM + 1

    def handle_close(self):
        print 'CLOSED'



if __name__ == "__main__":

	server1 = RelayServer('localhost', 9002)
	server2 = RelayServer('localhost', 9003)
	try:
		asyncore.loop()
	except:
		print 'EXIT NOW'
	

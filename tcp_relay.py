# -*- coding: utf-8 -*-
__author__ = 'sm9'

import asyncore, socket

CLIENT_SOCKS = []

def relay(sock, message):
    try:
        sock.sendall(message)
    except:
        sock.close()
        CLIENT_SOCKS.remove(sock)

class MyHandler(asyncore.dispatcher_with_send):
	def __init__(self, sock, clientNum):
		asyncore.dispatcher_with_send.__init__(self, sock)
		self.myNum = clientNum

	def handle_read(self):
		data = self.recv(8192)
		if data:
			target = 1 - self.myNum % 2
			relay(CLIENT_SOCKS[target], data)

class RelayServer(asyncore.dispatcher):

    def __init__(self, host, port):
		asyncore.dispatcher.__init__(self)
		self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
		self.set_reuse_addr()
		self.bind((host, port))
		self.listen(2)
		self.clientIssueNum = 0

    def handle_accept(self):
        pair = self.accept()
        if pair is not None:
			sock, addr = pair
			CLIENT_SOCKS.append(sock)
			print CLIENT_SOCKS.__str__()
			handler = MyHandler(sock, self.clientIssueNum)
			self.clientIssueNum += 1

    def handle_close(self):
        print 'CLOSED'



if __name__ == "__main__":

    server = RelayServer('localhost', 9001)
    asyncore.loop()

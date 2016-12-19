import socket
import select
import sys
import os
import glob
import threading

t_main = None
threads = []
max_size = 8192
request_name = ''
ServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
host = '127.0.0.1'
port = 61616
ServerSocket.bind((host, port))
ServerSocket.listen(5)
	
def main():
	# ServerSocket = Socket()
	# inputSocket = [ServerSocket]
	global ServerSocket
	global threads
	global request_name
	while True:
		read_ready, write_ready, exception = select.select(inputSocket, [], [])
		for sock in read_ready:
			if sock == ServerSocket: 
				client_socket, client_address = ServerSocket.accept()
				inputSocket.append(client_socket)
				for tt in threads:
					if not tt.isAlive():
						tt.join()
						threads.remove(tt)
			else:
				request = sock.recv(max_size)
				if request:
					print request
					request_header = request.split('\r\n')
					request_file = request_header[0].split(' ')
					request_name = request_file[1].split('/')
					request_access = request_name[1].split('.')
					response_content = ''
					if request_file[1] == '/index.html' or request_file[1] == '/' or request_file[1] == '':
						t = threading.Thread(target=HtmlResponse(sock,200,"index.html"))
						threads.append(t)
						t.start()
					elif request_access[1] == 'php':
						for filename in glob.glob('*.php'):
							t = threading.Thread(target=HtmlResponse(sock,403,"403.html"))
							threads.append(t)
							t.start()
					else:
						t = threading.Thread(target=HtmlResponse(sock,404,"404.html"))
						threads.append(t)
	 					t.start()


def HtmlResponse(conn_socket, status, file):
	f = open(file, 'r')
	response_content = f.read()
	f.close()
	content_length = len(response_content)
	return StatusCode(conn_socket, status, content_length, response_content)
	
def StatusCode(conn_socket,status, filesize, response_content):
	if (status==200):
		response_header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=UTF-8\r\nContent-Length:'+ str(filesize) + '\r\n\r\n'
	if (status==404):
		response_header = 'HTTP/1.1 404 Not Found\r\nContent-Type: text/html; charset=UTF-8\r\nContent-Length:' + str(filesize) + '\r\n\r\n'
	if (status==403):
		response_header = 'HTTP/1.1 403 Forbidden\r\nYou don`t have permission to access\r\nContent-Length:' + str(filesize) + '\r\n\r\n'
	print response_header
	conn_socket.sendall(response_header + response_content)
	return

ServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
host = '127.0.0.1'
port = 61616
ServerSocket.bind((host, port))
ServerSocket.listen(5)
inputSocket = [ServerSocket]

try:
	t_main = threading.Thread(main())
	t_main.start()
	threads.append(t_main)
except KeyboardInterrupt:
	for th in threads:
		th.join()
	ServerSocket.close()
	sys.exit(0)
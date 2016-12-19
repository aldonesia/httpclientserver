from socket import socket, AF_INET, SOCK_STREAM
import sys
import os

client_http = socket(AF_INET, SOCK_STREAM)

def method(jenis, message):
	if (jenis=='GET'):
		server_address = message[0].split(':')
		client_http.connect((server_address[0],int(server_address[1])))
		request = "GET /%s HTTP/1.0 \r\nHost: %s \r\n\r\n" % (message[2],message[0])
		client_http.send(request)
		data_recv = client_http.recv(4096)
		data = data_recv.split('\r\n\r\n')
		size = len(data[1])
		print data[0] + '\r\n\r\n'
		response_header = data[0].split('\r\n')
		#print response_header
		content_length = response_header[2].split(':')[1]
		if message[-1] == '' or message[-1] == 'index.html' or 'Not Found' in data[0]:
			print data[1]
	return


def main():
	try:
		while True:
			print '\r\nMethod : '
			jenis = raw_input()
			print '\r\nURL : '
			message = raw_input().partition('/')
			
			method(jenis, message)
	except KeyboardInterrupt:
		client_http.close()
		sys.exit(0)

main()
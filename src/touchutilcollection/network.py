
import socket

def check_port(portnumber:int):
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_probe:
		return bool( socket_probe.connect_ex( ( "127.0.0.1", int(portnumber))))

import socketserver
def get_free_port():
	with socketserver.TCPServer(("localhost", 0), socketserver.BaseRequestHandler ) as s:
		free_port = s.server_address[1]
	return free_port

import platform
def get_hostname():
	return platform.node()


import uuid
def get_computer_id():
	return str( uuid.getnode() )
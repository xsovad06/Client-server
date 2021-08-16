from socket import *
from sys import *

# Macros
BUFF_SIZE = 1024
PORT = 0

try:
	port_num = int(argv[1])
except:
	exit(500)
	
# Check port number, 0-1O23 are reserved for special services
if port_num > 1023:
	PORT = port_num
else:
	exit(500)

# Prepare for connection on appropriate port
with socket(AF_INET, SOCK_STREAM) as welcome_socket:
	welcome_socket.bind(('', PORT))
	welcome_socket.listen(1)

	# Infinity loop for request handling
	while True:
		conn_socket, client_addr = welcome_socket.accept()
		with conn_socket:
			data = conn_socket.recv(BUFF_SIZE)
			if not data:
				break
			message = data.decode('utf-8')
			message = message.split(" ", 3)
			answer = 'HTTP/1.1 '

			# Method identification (GET)
			if message[0] == 'GET':
				# Only HTTP requests accepted
				if message[2] != 'HTTP/1.1':
					answer += '400 Bad Request'
					answer = answer.encode('utf-8')
					conn_socket.sendall(answer)
					continue
				message = message[1].split("?")
				if message[0][1:7] == 'resolve':
					message = message[1].split("&")
					name = message[0].split("=")
					addr_type = message[1].split("=")
					if name[0] == 'name' and addr_type[0] == 'type':
						
						# Only "A" and "PTR" requests
						if addr_type[1] == 'A':
							try:
								IP = gethostbyname(name[1])
								answer += '200 OK\r\n\r\n' + name[1] + ':A=' + IP + '\n'
							except gaierror:
								answer += '404 Not Found'
						elif addr_type[1] == 'PTR':
							try:
								domain = gethostbyaddr(name[1])
								answer += '200 OK\r\n\r\n' + name[1] + ':PTR=' + domain[0] + '\n'
							except gaierror:
								answer += '404 Not Found'
						else:
							answer += '400 Bad Request'
					else:
						answer += '400 Bad Request'
				else:
					answer += '400 Bad Request'
			
			# Method identification (POST)
			elif message[0] == 'POST' and message[1] == '/dns-query':
				header = message[2].split("\r")
				
				# Only HTTP requests accepted
				if header[0] != 'HTTP/1.1':
					answer += '400 Bad Request'
					answer = answer.encode('utf-8')
					conn_socket.sendall(answer)
					continue
				message = message[3].split("\r\n\r\n")
				message = message[1].split("\n")
				answer += '200 OK\r\n\r\n'
				instr_solved = 0
				for item in message:
					if item == '':
						continue
					item = item.split(":")
					name = item[0]
					addr_type = item[1]

					# Only "A" and "PTR" requests
					if addr_type == 'A':
						try:
							IP = gethostbyname(name)
							answer += name + ':A=' + IP + '\n'
							instr_solved += 1
						except gaierror:
							continue
					elif addr_type == 'PTR':
						try:
							domain = gethostbyaddr(name)
							answer += name + ':PTR=' + domain[0] + '\n'
							instr_solved += 1
						except gaierror:
							continue
					else:
						continue
				if instr_solved == 0:
					answer = 'HTTP/1.1 400 Bad Request'
					answer = answer.encode('utf-8')
					conn_socket.sendall(answer)
					continue
			else:
				answer += '405 Method Not Allowed'

			# Sending answer back to client
			answer = answer.encode('utf-8')
			conn_socket.sendall(answer)

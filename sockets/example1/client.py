import socket

host = 'localhost'
port = 5555

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect((host, port))
clientsocket.send(bytes('Hello socket!', encoding='UTF-8'))
data = clientsocket.recv(1024)
clientsocket.close()
print(data)

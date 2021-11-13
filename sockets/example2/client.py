import socket

host = 'localhost'
port = 5555

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    clientsocket.connect((host, port))
except socket.error as e:
    print(e)

response = clientsocket.recv(1024)
while True:
    message = input('Enter message: ')
    if not message:
        break
    clientsocket.send(str.encode(message))
    response = clientsocket.recv(1024)
    print(response.decode('utf-8'))

clientsocket.close()

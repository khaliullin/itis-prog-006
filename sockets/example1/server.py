import socket

host = '127.0.0.1'
port = 5555

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind((host, port))
serversocket.listen(5)

print('Server is running. Press ctrl+c to stop')
print('Listening for connections')

while True:
    conn, address = serversocket.accept()
    print(f'New connection: {address}')
    data = conn.recv(1024)
    print(str(data))
    conn.send(data.upper())
    conn.close()

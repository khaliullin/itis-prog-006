import socket
from _thread import start_new_thread

host = '127.0.0.1'
port = 5555
thread_count = 0

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind((host, port))
serversocket.listen(5)

print('Server is running. Press ctrl+c to stop')
print('Listening for connections')


def client_talk(connection):
    connection.send(str.encode('Connection started'))
    while True:
        data = connection.recv(1024)
        print(str(data))
        if not data:
            break
        response_message = f'Server message: {data.upper().decode("utf-8")}'
        connection.send(str.encode(response_message))
    connection.close()


while True:
    conn, address = serversocket.accept()
    print(f'New connection established: {address}')
    start_new_thread(client_talk, (conn, ))
    thread_count += 1
    print(f'Thread number: {thread_count}')

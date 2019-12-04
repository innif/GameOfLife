import socket

def run():
    host = socket.gethostname()
    port = 5000  # set port number

    server_socket = socket.socket()
    server_socket.bind((host, port))  # bind host address and port together

    server_socket.listen(2) # max number of clients

    print('Waiting for Player 1')
    conn1, address1 = server_socket.accept()  # accept new connection
    print("Player 1 connected with address " + str(address1))

    print('Waiting for Player 2')
    conn2, address2 = server_socket.accept()  # accept new connection
    print("Player 2 connected with address " + str(address2))

    while True:
        data = conn1.recv(1024).decode() # receive with maximum 1024 bytes
        if not data:
            # if data is not received break
            break
        print("from connected user: " + str(data))
        data = input(' -> ')
        conn1.send(data.encode())  # send data to the client

    conn1.close()  # close the connection


if __name__ == '__main__':
    run()
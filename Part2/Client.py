import socket

SERVER_ADDR = "127.0.0.1"
SERVER_PORT = 8080
CLIENT_ADDR = "127.0.0.1"
CLIENT_PORT = 8081


with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as client:
    client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Bind client
    client.bind((CLIENT_ADDR, CLIENT_PORT))
    print("socket binded to %s" % (CLIENT_PORT))

    # connect to server
    client.connect((SERVER_ADDR, SERVER_PORT))

    # recv message
    data = client.recv(1024)

    # if message recived print message
    if data:
        print(f"Received: {data}")

    # safe close
    client.close()

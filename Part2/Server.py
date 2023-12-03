import socket

HOST_ADDR = "127.0.0.1"
HOST_PORT = 8080


class Server:
    # Initializing
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # bind server
        self.sock.bind((HOST_ADDR, HOST_PORT))
        print("socket binded to %s" % (HOST_PORT))

        # listen to clients
        self.sock.listen(5)
        print("socket is listening")
        while True:
            # accept connection
            conn, client_addr = self.sock.accept()
            print("Got connection from", client_addr)

            # send message
            conn.send(b"Thank you for connecting")
            conn.close()

    # Deleting (Calling destructor)
    def __del__(self):
        self.sock.close()


if __name__ == "__main__":
    try:
        s = Server()
    except KeyboardInterrupt:
        print("losing server...")

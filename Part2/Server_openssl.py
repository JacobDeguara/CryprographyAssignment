import socket
import ssl

HOST_ADDR = "127.0.0.1"
HOST_PORT = 8080

# OpenSSL context certification
context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.load_cert_chain(
    certfile="Part2/Certification_Authority/myCA.pem",
    keyfile="Part2/Certification_Authority/myCA.key",
)


class Server:
    # starts server
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # wrapping connection with OpenSSL context
        with context.wrap_socket(self.sock, server_side=True) as server:
            # bind server
            server.bind((HOST_ADDR, HOST_PORT))
            print("socket binded to %s" % (HOST_PORT))

            # start listening
            server.listen(5)
            print("socket is listening")

            while True:
                # accept connection
                conn, client_addr = server.accept()
                print("Got connection from", client_addr)

                # send message
                conn.send(b"Thank you for connecting")
                conn.close()

    # closes server safely
    def __del__(self):
        self.sock.close()


if __name__ == "__main__":
    try:
        s = Server()
    except KeyboardInterrupt:
        print("losing server...")

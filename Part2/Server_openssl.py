import socket
import ssl

HOST_ADDR = "127.0.0.1"
HOST_PORT = 8080


context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.load_cert_chain(
    certfile="Certification_Authority/myCA.pem",
    keyfile="Certification_Authority/myCA.key",
)

# Setup socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # wrap socket with ssl wrapper
    with context.wrap_socket(sock, server_side=True) as server:
        # bind server
        server.bind((HOST_ADDR, HOST_PORT))
        print("socket binded to %s" % (HOST_PORT))
        server.listen(5)
        print("socket is listening")

        while True:
            # accept connection
            conn, client_addr = server.accept()
            print("Got connection from", client_addr)
            # send message
            conn.send(b"Thank you for connecting")
            conn.close()

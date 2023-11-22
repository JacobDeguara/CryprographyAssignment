import socket
import ssl

SERVER_ADDR = "127.0.0.1"
SERVER_PORT = 8080


context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
context.load_cert_chain(
    certfile="Certification_Authority/myCA.pem",
    keyfile="Certification_Authority/myCA.key",
)
context.check_hostname = False  # Verifying host name disables as it is causing issues
context.verify_mode = ssl.CERT_NONE

with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    with context.wrap_socket(sock, server_hostname="127.0.0.1:8080") as client:
        client.bind(("127.0.0.1", 8081))
        print("socket binded to %s" % (8081))
        client.connect(("127.0.0.1", 8080))
        data = client.recv(1024)
        if data:
            print(f"Received: {data}")
        client.close()

import socket
import ssl

SERVER_ADDR = "127.0.0.1"
SERVER_PORT = 8080
CLIENT_ADDR = "127.0.0.1"
CLIENT_PORT = 8081

# OpenSSL context certification
context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
context.load_cert_chain(
    certfile="Part2/Certification_Authority/myCA.pem",
    keyfile="Part2/Certification_Authority/myCA.key",
)
context.check_hostname = False  # Verifying host name disables as it is causing issues
context.verify_mode = ssl.CERT_NONE

with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # wrapping connection with OpenSSL context
    with context.wrap_socket(
        sock, server_hostname=(SERVER_ADDR + str(SERVER_PORT))
    ) as client:
        # bind client
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

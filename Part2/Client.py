"""
import socket
import ssl

hostname = "127.0.0.1:8443"
# PROTOCOL_TLS_CLIENT requires valid cert chain and hostname
context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
context.load_verify_locations(
    "/home/jacob/coding/cryptography/Assignment/Part2/cert.pem"
)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
    with context.wrap_socket(sock, server_hostname=hostname) as ssock:
        print(ssock.version())
"""

# Import socket module
import socket

# Create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
port = 8081
s.bind(("127.0.0.1", port))
# Define the port on which you want to connect
port = 8080

# connect to the server on local computer
s.connect(("127.0.0.1", port))

# receive data from the server
print(s.recv(1024))

# close the connection
s.close()

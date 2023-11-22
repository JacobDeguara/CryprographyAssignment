"""
import socket
import ssl

context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(
    "/home/jacob/coding/cryptography/Assignment/Part2/cert.pem",
    "/home/jacob/coding/cryptography/Assignment/Part2/cert.pem",
)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
    sock.bind(("127.0.0.1", 8443))
    sock.listen(5)
    with context.wrap_socket(sock, server_side=True) as ssock:
        conn, addr = ssock.accept()
"""

# first of all import the socket library
import socket

# next create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
print("Socket successfully created")

# reserve a port on your computer in our
# case it is 40674 but it can be anything
port = 8080

# Next bind to the port
# we have not typed any ip in the ip field
# instead we have inputted an empty string
# this makes the server listen to requests
# coming from other computers on the network
s.bind(("127.0.0.1", port))
print("socket binded to %s" % (port))

# put the socket into listening mode
s.listen(5)


# a forever loop until we interrupt it or
# an error occurs
while True:
    # Establish connection with client.
    c, addr = s.accept()
    print("Got connection from", addr)

    # send a thank you message to the client.
    c.send(b"Thank you for connecting")

    # Close the connection with the client
    c.close()

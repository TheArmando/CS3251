import sys
import socket
import time

# our TCP and UDP versions will share much of the same code for command line parsing and user interaction.
# However, your UDP implementation will have to deal with lost request messages or non-responding server.
# The UDP client should set a timeout for receiving a response.
# If the client does not receive a response within 2 seconds, it should retry the same query 3 times.
# After 3 unsuccessful requests, the client should print an error message and exit.
# A good way to test your client in this situation is to run it without the server.
# Does your client handle this gracefully?

# https://wiki.python.org/moin/UdpCommunication
UDP_IP = "0.0.0.0"
UDP_PORT = 8090
BUFFER_SIZE = 4096

if __name__ == "__main__":
    while True:

        clock = time.time()
        sock = socket.socket(socket.AF_INET,  # Internet
                             socket.SOCK_DGRAM)  # UDP

        sock.bind((UDP_IP, UDP_PORT))

        while True:
            data, addr = sock.recvfrom(BUFFER_SIZE)
            if time.time() - clock >= 3 and not data:
                break
            elif data:
                clock = time.time()
            print("recieved message", data)
            sock.sendto("done", (UDP_IP, UDP_PORT))


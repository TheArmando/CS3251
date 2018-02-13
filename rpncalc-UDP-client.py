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
UDP_PORT = 5005
BUFFER_SIZE = 4096

if __name__ == "__main__":
    UDP_IP = str(sys.argv[1])
    UDP_PORT = int(sys.argv[2])
    procedure = str(sys.argv[3])

    sock = socket.socket(socket.AF_INET,  # Internet
                         socket.SOCK_DGRAM)  # UDP

    sock.settimeout(2)

    connSendCount = 0
    # clock = time.time()

    while connSendCount <= 3:
        # print(time.time() - clock)
        try:
            sock.sendto(procedure, (UDP_IP, UDP_PORT))
            connSendCount += 1
            print("Attemping Send")
            data, addr = sock.recvfrom(BUFFER_SIZE)
            print("Finished Receiving")
            if data:
                # clock = time.time()
                connSendCount = 0
            if data == "done":
                exit(0)
        except socket.timeout:
            print("Connection timed out.")
        except socket.error:
            print("Connection closed.")
            exit(1)

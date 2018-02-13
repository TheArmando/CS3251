import sys
import socket

# You should support addition, subtraction, multiplication and division.
# You can limit the application to support only integer (of arbitrary value) input and output.

# Sudo code from the wikipedia article provided in the pdf
# for each token in the postfix expression:
#   if token is an operator:
#     operand_2 <- pop from the stack
#     operand_1<- pop from the stack
#     result<- evaluate token with operand_1 and operand_2
#     push result back onto the stack
#   else if token is an operand:
#     push token onto the stack
# result<- pop from the stack

# https://wiki.python.org/moin/TcpCommunication

TCP_IP = '0.0.0.0'
TCP_PORT = 8090
BUFFER_SIZE = 4096


def rpn_parse(formula):
    stack = []
    i = 0
    while i < len(formula):
        char = formula[i]
        if char == '+' or char == '-' or char == '*' or char == '/':
            operand1 = int(stack.pop())
            operand2 = int(stack.pop())
            if char == '+':
                stack.append(operand1 + operand2)
            if char == '-':
                stack.append(operand1 - operand2)
            if char == '*':
                stack.append(operand1 * operand2)
            if char == '/':
                stack.append(operand1 / operand2)
        elif char != " ":  # if its a number
            full_number = char
            # This bit of code is meant to grab the whole number if it consists of multiple digits
            if i != (len(formula) - 1) and formula[i + 1] != " ":
                full_number = ""
                while char != " ":
                    char = formula[i]
                    full_number += char
                    i += 1
                i -= 1
            stack.append(full_number)
        i += 1
    return stack.pop()


if __name__ == "__main__":
    TCP_IP = str(sys.argv[1])
    TCP_PORT = int(sys.argv[2])
    procedure = str(sys.argv[3])


    #print(procedure)
    # This is testing the parser
    #print(rpn_parse(procedure))

    # TODO check the input to make sure that it is in the proper format

    while True:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # connect()
            sock.connect((TCP_IP, TCP_PORT))
            expression = ""
            j = 0
            answer = 0
            for i in range(len(procedure)):
                if procedure[i] == "-" or procedure[i] == "+" or procedure[i] == "/" or procedure[i] == "*":
                    expression = procedure[j:i+1]  # get the first expression
                    j = i+1
                    if answer != 0:
                        sock.send(str(answer) + " " + expression)
                    else:
                        sock.send(expression)
                    answer = int(sock.recv(BUFFER_SIZE))
                    # if procedure[i] == "-":
                    #     answer -= int(sock.recv(BUFFER_SIZE))
                    # if procedure[i] == "+":
                    #     answer += int(sock.recv(BUFFER_SIZE))
                    # if procedure[i] == "*":
                    #     answer *= int(sock.recv(BUFFER_SIZE))
                    # if procedure[i] == "/":
                    #     answer /= int(sock.recv(BUFFER_SIZE))
                    #print("current answer", answer)

            print("Solution: " + str(answer))
        except socket.error:
            print("Connection closed.")
            exit(1)


# Code is based off
#/ https://docs.python.org/2/howto/sockets.html
# class mysocket:
#     '''demonstration class only
#       - coded for clarity, not efficiency
#     '''
#
#     def __init__(self, sock=None):
#         if sock is None:
#             self.sock = socket.socket(socket.AF_INET, socket.SOCK_RAW)
#         else:
#             self.sock = sock
#
#     def connect(self, host, port):
#         self.sock.connect((host, port))
#
#     def mysend(self, msg):
#         totalsent = 0
#         while totalsent < MSGLEN:
#             sent = self.sock.send(msg[totalsent:])
#             if sent == 0:
#                 raise RuntimeError("socket connection broken")
#             totalsent = totalsent + sent
#
#     def myreceive(self):
#         chunks = []
#         bytes_recd = 0
#         while bytes_recd < MSGLEN:
#             chunk = self.sock.recv(min(MSGLEN - bytes_recd, 2048))
#             if chunk == '':
#                 raise RuntimeError("socket connection broken")
#             chunks.append(chunk)
#             bytes_recd = bytes_recd + len(chunk)
#         return ''.join(chunks)
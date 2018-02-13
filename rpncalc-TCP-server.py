import sys
import socket

TCP_IP = '0.0.0.0'
TCP_PORT = 8090
BUFFER_SIZE = 4096


# https://wiki.python.org/moin/TcpCommunication


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
    #TCP_IP = str(sys.argv[1])
    #TCP_PORT = int(sys.argv[2])

    while True:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((TCP_IP, TCP_PORT))
        sock.listen(1)

        connection, address = sock.accept()
        print 'Connection address:', address

        aggregate_answer = 0

        while 1:
            data = connection.recv(BUFFER_SIZE)
            if not data: break
            # print "received data:", data
            print("Executing", data)
            if aggregate_answer == 0:
                solution = rpn_parse(data)
            else:
                solution = rpn_parse(str(aggregate_answer) + " " + data)
            print("solution calculated:",  solution)
            # if aggregate_answer == 0:
            aggregate_answer = solution
            # else:
            #     if data[-1] == "*":
            #         aggregate_answer *= int(solution)
            #     if data[-1] == "/":
            #         aggregate_answer /= int(solution)
            #     if data[-1] == "+":
            #         aggregate_answer += int(solution)
            #     if data[-1] == "-":
            #         aggregate_answer -= int(solution)
            print("current aggregate answer:", aggregate_answer)
            connection.send(str(aggregate_answer))  # echo
        connection.close()

from struct import *
import socket

# Server IP, port
serverIP = '127.0.0.1'
serverPort = 1000
# Flag for closing socket
close = False

# Server socket
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind((serverIP, serverPort))
print("The server is waiting for client on port", str(serverPort))

# Listen for connections
serverSocket.listen()

while not close:
    # Accept connection, client's connection and address
    connection, address = serverSocket.accept()

    # Print info
    print("Server Socket: ", connection.getsockname())
    print("Client Socket: ", connection.getpeername())

    # Execute all 4 operations
    while True:
        # Receive the 2 HH (type, length) = 4 bytes
        message = connection.recv(4)

        # Unpack 2 short - length, type
        message_type, message_length = unpack('HH', message)

        message = connection.recv(message_length - 4 + 1)

        # Unpack the rest of the message
        message_id, int1, int2, operator = unpack('Ihhx1s', message)

        # Decode, to print operation
        operator = operator.decode('utf-8')
        int1_str = str(int1)
        int2_str = str(int2)
        print('Operation received: ' + int1_str + ' ' + operator + ' ' + int2_str)

        # Operation result
        result = 0
        # Implement operations
        if operator == '+':
            result = int1 + int2
        elif operator == '-':
            result = int1 - int2
        elif operator == '*':
            result = int1 * int2
        elif (operator == '/') & (int2 != 0):
            result = int1 / int2
        # Print result
        print('Send result: ' + str(result))

        # Create response to client
        message_type = 1
        # Detect errors
        message_response_code = 0
        if (int1 > 30000) | (int1 < 0):
            message_response_code = 1
        if (int2 > 30000) | (int2 < 0):
            message_response_code = 2
        if (operator == '/') & (int2 == 0):
            message_response_code = 3

        # Result to float to send decimal part in division
        result = float(result)
        message = pack('HHIf', message_type, message_response_code, message_id, result)

        # Send the response
        err = connection.sendall(message)
        # Print errors
        print('Error: ' + str(err))

# Close socket
close = True
connection.close()
serverSocket.close()
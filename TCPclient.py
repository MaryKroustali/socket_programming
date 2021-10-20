from struct import *
import socket

# Server IP, port
serverIP = '127.0.0.1'
serverPort = 1000

# TCP socket connect to server
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((serverIP, serverPort))

# User data
message_type = 0  # 0 for message, 1 for response
message_id = 1
print('Insert first integer (0-30000):')
int1 = int(input())
print('Insert second integer (0-30000):')
int2 = int(input())

# Operations to execute
operations = ["+", "-", "*", "/"]

# Loop executed for each operator
for operator in operations:
    # Calculate message length (4bytes (type,length)  + 4bytes (id) + 4bytes (int1,int2)) + 1byte (operator)
    message_length = 2*2 + 2*4 + 1
    # Encode operator symbol
    number_of_bytes = bytes(operator, 'utf-8')

    # Pack message to send
    message = pack('HHIhhx1s', message_type, message_length, message_id, int1, int2, number_of_bytes)

    # Print operation
    int1_str = str(int1)
    int2_str = str(int2)
    print('Operation sent: ' + int1_str + ' ' + operator + ' ' + int2_str)

    # Send message
    clientSocket.sendall(message)

    # Client will receive 2*2 (HH(type, response code)) + 4 (I(id)) + 4 (f(operation result)) = 12 bytes
    response = clientSocket.recv(12)
    message_type, message_response_code, message_response_id, result = unpack('HHIf', response)

    # Check if response is for this message (by id)
    if message_id == message_response_id:
        # Print error based on response code
        if message_response_code == 0:  # No errors found
            if result.is_integer():   # For int result (+, -, *)
                result = int(result)   # Return int value
            print('Result: ' + str(result))
        elif message_response_code == 1:
            print("Error: First integer is not 0-30000!")
        elif message_response_code == 2:
            print("Error: Second integer is not 0-30000!")
        elif message_response_code == 3:
            print("Error: Operation division, second integer must not be 0!")
    else:
        print("This is response for another message")

print("\nOperation completed. Closing socket...")
clientSocket.close()

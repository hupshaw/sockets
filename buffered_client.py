from socket import * 
from struct import pack, unpack

class BufferedTCPClient:

    def __init__(self, server_host='localhost', server_port=36001, buffer_size=1024):
        self.buffer_size = buffer_size
        self.my_sock = socket(AF_INET, SOCK_STREAM) # create socket
        self.my_sock.connect((server_host, server_port)) #establish TCP Connection

    # This method is called by the autograder. You must implement it, and you cannot change the method signature. It should accept a message
    # from the user, which is packed according to the format specified for this assignment and then sent into the socket.
    # TODO: * Send a message to the server containing the message passed in to the function. 
    #           * Remember to pack it using the format defined in the instructions. 
    def send_message(self, message):
        print("CLIENT: Attempting to send a message...")
        
        # while len(message) > self.buffer_size:
        #     print("Send:")

        message_length = len(message)
        packed_data = pack("!H"+str(message_length)+"s", message_length, message.encode())
        self.my_sock.send(packed_data)

        #print("???")


    # This method is called by the autograder. You must implement it, and you cannot change the method signature. It should wait to receive a 
    # message from the socket, which is then returned to the user. It should return two values: the message received and whether or not it was received 
    # successfully. In the event that it was not received successfully, return an empty string for the message.
    # TODO: 
    #      * The server may send a message that exceeds the buffer length, so you must buffer 
    #       incoming messages until you have received all of a given message.
    #     * Remember that we're sending packed messages back and forth, for the format defined in the assignment instructions. You'll have to unpack
    #      the message and return just the string. Don't return the raw response from the server.
    #       * Handle any errors associated with the server disconnecting
    def receive_message(self):
        print("CLIENT: Attempting to receive a message...")
        try:
            data = self.my_sock.recv(self.buffer_size) 
            if data:
                length = data[:2]
                length = unpack("!H", length)[0]
                print(length)
                payload = data[2:]
                while len(payload) < length:
                    data = self.my_sock.recv(self.buffer_size)
                    payload += data
                message = payload.decode()
                print(message)
                return message, True
            else:
                return "", False
        except ConnectionResetError as e:
            return "", False
        

    # This method is called by the autograder. You must implement it, and you cannot change the method signature. It should close your socket.
    # TODO: Close your socket
    def shutdown(self):
        print("Client: Attempting to shut down...")
        self.my_sock.close()

        
if __name__ == "__main__":
    l = BufferedTCPClient(server_host="localhost", server_port=36001)

    l.send_message("Four score and seven years ago")
    response = l.receive_message()
    print(response)

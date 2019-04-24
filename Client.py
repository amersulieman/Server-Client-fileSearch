import socket
import sys
class Client():
    def __init__(self,clientAddress,client_socket):
        self.clientAddress=clientAddress
        self.socket = client_socket
    def send(self):
        try:
            self.socket.send(b"input.txt")
            print("File Name sent successfully...")
        except:
            print("Problem sending file name...")
            self.socket.close()
            sys.exit(1)

    def receive(self):
        try:
            data =self.socket.recv(4096).decode()
            print(data)
        except:
            print("Problem receiving...")
            self.socket.close()
            sys.exit(1)

clt_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
localHost = socket.gethostname()
ip_address = socket.gethostbyname(localHost)
serverAdds = (ip_address, 1357)
clt_socket.connect(serverAdds)
print("Connecting to {} with {}".format(localHost,ip_address))
myclient = Client(ip_address,clt_socket)
myclient.send()
myclient.receive()
clt_socket.close()
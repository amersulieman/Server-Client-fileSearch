import socket
import sys
import os
class Client():

    def __init__(self):
        self.localHostAddress= None
        self.localHostName = None
        self.clt_socket = None
        self.portToConnectTo = 1357
        self.fileLookingFor = sys.argv[1]

    def setUpSocketAndConnect(self):
        #create Client Socket
        self.clt_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.localHostName = socket.gethostname()
        self.localHostAddress = socket.gethostbyname(self.localHostName)
        serverAddress = (self.localHostAddress,self.portToConnectTo)
        try:
            self.clt_socket.connect(serverAddress)
            print("Connecting to {} with {}".format(self.localHostName,self.localHostAddress))
        except:
            print("Problem Connecting to server....")
            sys.exit()

    def send(self):
        try:
            self.clt_socket.send(bytes(self.fileLookingFor,"utf-8"))
            print("Asking server for file {} ...".format(self.fileLookingFor))
        except:
            print("Problem sending file name...")
            self.clt_socket.shutdown(socket.SHUT_RDWR)
            self.clt_socket.close()
            sys.exit()

    def receive(self):
        if self.clt_socket.recv(16).decode()=="-1":
            print("The file {} not available....".format(self.fileLookingFor))
        else:
            try:
                fileName,extension= os.path.splitext(self.fileLookingFor)
                totalData = b""
                while True:
                    data=self.clt_socket.recv(4096)
                    if not data:
                        break
                    totalData+=data
                try:
                    with open(fileName+"_clt"+extension,"wb") as myFile:
                        myFile.write(totalData)
                    print("Client Received File...")
                except:
                    print("Problem saving file data...")
            except:
                print("Problem receiving...")



if len(sys.argv)<2:
    print("Please provide File name.....")
    sys.exit()
clt = Client()
clt.setUpSocketAndConnect()
clt.send()
clt.receive()
clt.clt_socket.close()


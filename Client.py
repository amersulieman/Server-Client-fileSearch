'''
@author Amer Sulieman
@version 04/20/2019

Client.py   
    Client side of a sever-client communication
    The client only asks for a file from the server
    and expect server to send the client the file
    if it exists...
'''
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

    #Set up client socket and connect it to the server end using the given port in client object
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
            print("Problem Connecting to server....\nServer might be asleep....")
            sys.exit()

    #Send the filname as bytes and wait for server response
    def send(self):
        try:
            self.clt_socket.send(bytes(self.fileLookingFor,"utf-8"))
            print("Asking server for file {} ...".format(self.fileLookingFor))
        except:
            print("Problem sending file name...")
            self.clt_socket.shutdown(socket.SHUT_RDWR)
            self.clt_socket.close()
            sys.exit()

    #if received the confirmation that the file exists then creat new file and save received data to it
    def receive(self):
        confirmationFile = self.clt_socket.recv(1096).decode()
        if confirmationFile == "True":
            try:
                #breaks file name and its extension for saving different name
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
                print("Problem receiving data from server...")
        else:
            print("The File {} is not available".format(self.fileLookingFor))

#checks if file name given to command line args
if len(sys.argv)<2:
    print("Please provide File name.....")
    sys.exit()
clt = Client()
clt.setUpSocketAndConnect()
clt.send()
clt.receive()
clt.clt_socket.close()


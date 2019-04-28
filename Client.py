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
        self.fileLookingFor = sys.argv[1] #argument in command line for file name

    #Set up client socket and connect it to the server using the given port in client object
    def setUpSocketAndConnect(self):
        #create Client Socket
        self.clt_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.localHostName = socket.gethostname()
        self.localHostAddress = socket.gethostbyname(self.localHostName)
        #server address and port to connect to
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
            #send file name encoded
            self.clt_socket.send(bytes(self.fileLookingFor,"utf-8"))
            print("Asking server for file {} ...".format(self.fileLookingFor))
        except:
            print("Problem sending file name...")
            #shutdown connection if problem in sending
            self.clt_socket.shutdown(socket.SHUT_RDWR)
            self.clt_socket.close()
            sys.exit()

    #if received the confirmation that the file exists then create new file and save received data to it
    def receive(self):
        #receive first confirmation if file exists
        confirmationFile = self.clt_socket.recv(1096).decode()
        if confirmationFile == "True":
            try:
                #breaks file name and its extension for saving different name
                fileName,extension= os.path.splitext(self.fileLookingFor)
                totalData = b"" #data recieved in bytes
                while True:
                    data=self.clt_socket.recv(4096)
                    if not data:
                        break
                    totalData+=data
                try:
                    # after all data received save it to a file with name of old file and "_clt" added to it
                    with open(fileName+"_clt"+extension,"wb") as myFile:
                        myFile.write(totalData)
                    print("Client Received File...")
                except:
                    #if writing data caused a problem
                    print("Problem saving file data...")
            except:
                #if problem in receiving from socket occured
                print("Problem receiving data from server...")
        else:
            # if the file was not available which is known from confirmation
            print("The File {} is not available".format(self.fileLookingFor))

#checks if file name given to command line args
if len(sys.argv)<2:
    print("Please provide File name.....")
    sys.exit()

#create client object    
clt = Client()
#create client socket and connect to server
clt.setUpSocketAndConnect()
#send file looking for
clt.send()
#recieve file or if it doesnt exist
clt.receive()
#close connection
clt.clt_socket.close()


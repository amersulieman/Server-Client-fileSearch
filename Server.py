'''
@author Amer Sulieman
@version 04/20/2019
Server.py   
    Server side of a sever-client communication
    The server only receives filename that the client
    is looking for and send first confirmation if
    it exists, if yes, then send the file data
    in bytes...
'''
import socket
import os.path as path
import sys
class Server():
    def __init__(self):
        self.serverAddress=None
        self.portListening = 1357
        self.localHostName = None
        self.serverSocket = None
        self.socketConnection =None
        self.fileName= None

    #setup server socket
    def setUpSocket(self):
        #create server socket
        self.serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.localHostName = socket.gethostname()
        self.serverAddress = socket.gethostbyname(self.localHostName)
        print("working with {}, {}".format(self.localHostName,self.serverAddress))
        print("Starting up {} with port {}".format(self.serverAddress,self.portListening))
        try:
            self.serverSocket.bind((self.serverAddress,self.portListening))
        except:
            print("Problem binding port number to server address...")
            sys.exit()

    #setup connecttion with the socket created, and wait for connection from client
    def setUpconnection(self):
        #accept one if multiple connections came
        try:
            self.serverSocket.listen(1)
            print("WAITING FOR CONNECTIONS.......")
            self.serverSocket.settimeout(40) #timeout after 40 seconds if no connections
            self.socketConnection,clt_adds = self.serverSocket.accept()
            print("Connection from {}".format(clt_adds))
        except:
            print("Time out waiting for connection.....")
            sys.exit()

    #receive file name that the client looking for 
    def receive(self):
        try:
            receivedName=self.socketConnection.recv(4096).decode() 
            self.fileName=receivedName
            print("Server Searching for the file...")
        except:
            print("Problem receiving...")
            self.socketConnection.shutdown(socket.SHUT_RDWR)
            self.socketConnection.close()

    #check if file exists and send confirmation
    #if exists then send file
    def send(self):
        confirmation = self.fileConfirm()
        self.socketConnection.send(bytes(confirmation,"utf-8"))
        if confirmation=="True":
            with open(self.fileName,"rb")as myFile:
                try:
                    self.socketConnection.sendfile(myFile)
                    print("Server Sent File successfully...")
                except:
                    print("Server has issues sending...")
                    
    #method to check if file exist
    def fileConfirm(self):
        if path.isfile(self.fileName):
            return "True"
        else: return "False"
myserver = Server()
myserver.setUpSocket()
myserver.setUpconnection()
myserver.receive()
myserver.send()
myserver.socketConnection.close()
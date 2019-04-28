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
            #bind address and port to socket
            self.serverSocket.bind((self.serverAddress,self.portListening))
        except:
            print("Problem binding port number to server address...")
            sys.exit()

    #setup connecttion with the socket created, and wait for connection from client
    def setUpconnection(self):
        try:
            #accept one connection if multiple connections came before accept method
            self.serverSocket.listen(1)
            print("WAITING FOR CONNECTIONS.......")
            self.serverSocket.settimeout(40)  #timeout after 40 seconds if no connections
            #new socket and its address return after connection is made
            self.socketConnection,clt_adds = self.serverSocket.accept()
            print("Connection from {}".format(clt_adds))
        except:
            print("Time out waiting for connection.....")
            sys.exit()

    #receive file name that the client looking for 
    def receive(self):
        try:
            #decode the sent bytes (file name)
            receivedName=self.socketConnection.recv(4096).decode() 
            self.fileName=receivedName
            print("Server Searching for the file...")
        except:
            print("Problem receiving...")
            #shuts connection if problem occured receiving
            self.socketConnection.shutdown(socket.SHUT_RDWR)
            self.socketConnection.close()

    #if exists then send file
    def send(self):
        #check if file exists and send confirmation
        confirmation = self.fileConfirm() #different function
        self.socketConnection.send(bytes(confirmation,"utf-8")) # send true or false encoded for confirmation
        if confirmation=="True":    # if confired file exists then open it in binary
            with open(self.fileName,"rb")as myFile:
                try:
                    #send the file to client 
                    self.socketConnection.sendfile(myFile)
                    print("Server Sent File successfully...")
                except:
                    print("Server has issues sending...")
                    
    #method to check if file exist
    def fileConfirm(self):
        if path.isfile(self.fileName):
            return "True"
        else: return "False"

#create server object            
myserver = Server()
#setup socket
myserver.setUpSocket()
#look for connection
myserver.setUpconnection()
#receive from client if connection established
myserver.receive()
#send file if exists
myserver.send()
#close connection
myserver.socketConnection.close()
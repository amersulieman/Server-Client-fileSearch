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

    def setUpconnection(self):
        #accept one if multiple connections came
        try:
            self.serverSocket.listen(1)
            print("WAITING FOR CONNECTIONS.......")
            self.serverSocket.settimeout(40)
            self.socketConnection,clt_adds = self.serverSocket.accept()
            print("Connection from {}".format(clt_adds))
        except:
            print("Time out waiting for connection.....")
            sys.exit()

    def receive(self):
        try:
            receivedName=self.socketConnection.recv(4096).decode()
            self.fileName=receivedName
            print("Server Searching for the file...")
        except:
            print("Problem receiving...")
            self.socketConnection.shutdown(socket.SHUT_RDWR)
            self.socketConnection.close()
            
    def send(self):
        confirmation = self.fileConfirm()
        print(confirmation)
        print("Server sending confirtmation if file exists...")
        self.socketConnection.send(bytes(confirmation,"utf-8"))
        if confirmation=="True":
            with open(self.fileName,"rb")as myFile:
                try:
                    self.socketConnection.sendfile(myFile)
                    print("Server Sent File successfully...")
                except:
                    print("Server has issues sending...")

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
import socket
import socket
import os.path as path
class Server():
    def __init__(self,sAdds,port,connection):
        self.serverAddress=sAdds
        self.portListening = port
        self.connection = connection
        self.fileName= None
    def send(self):
        if path.isfile("./"+self.fileName):
            with open("./"+self.fileName,"rb")as myFile:
                try:
                    self.connection.sendfile(myFile)
                except:
                    self.connection.send(b"Server has issues sending...")
        else:
            self.connection.send(b"File Does not Exist!")

    def receive(self):
        try:
            receivedName=self.connection.recv(4096).decode()
            self.fileName=receivedName
        except:
            self.connection.send(b"Problem receiving...")
#create server socket
serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#get the name of the host where python interpreter works
localHost= socket.gethostname()
#get the ip address according to the name
ip_address = socket.gethostbyname(localHost)
print("working with {},{}".format(localHost,ip_address))
serverAddress = (ip_address, 1357)
print("Starting up {} with port {}".format(serverAddress[0],serverAddress[1]))
serverSocket.bind(serverAddress)
#accept one if multiple connections came
serverSocket.listen(1)
print("WAITING FOR CONNECTIONS.......")
conn,clt_adds = serverSocket.accept()
print("Connection from {}".format(clt_adds))
myserver = Server(ip_address,1357,conn)
myserver.receive()
myserver.send()
conn.close()
serverSocket.close()

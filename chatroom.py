from Files.Data.imports import *

class ClientHandler(Thread):

    def __init__(self,client,address):
        global sockets # sockets is the list of all client's connected to server
        global addresses # addresses is the list of address of all client's
        global connected_clients # connected_clients -> all the clients who found pairs
        Thread.__init__(self)
        self._client = client
        self._address = address
        sockets.append(self._client)
        addresses.append(self._address)

    def run(self):
        self._client.send(b'Welcome to the chatroom!\n')
        
        while 1:
            if len(sockets)%2 == 0:
                print("i am here",len(sockets))
                if [sockets[-1],sockets[-2]] not in connected_clients:
                    connected_clients.append([sockets[-1],sockets[-2]])
            print("ACTIVE CLIENTS :", len(sockets), self._address)
            try:
                message = self._client.recv(BUFSIZE)
                message = message.decode('utf-8')
            except:
                message = "exit"
            # print('\n\n','Sockets = ',sockets)
            if not message or message == "exit" :
                print("Client Disconnected.")
                addIndex=sockets.index(self._client)
                del sockets[addIndex]
                del addresses[addIndex]
                for y in connected_clients:
                    if y[0] == self._client:
                        sockets.remove(y[1])
                        sockets.append(y[1])
                        connected_clients.remove(y)
                        break
                    elif y[1] == self._client:
                        socket.remove(y[0])
                        socket.append(y[0])
                        connected_clients.remove(y)
                        break
                self._client.close()
                break
            else:
                message = f"{self._address[1]} : {message}"
                for x in sockets:
                    for y in connected_clients:
                        if x != self._client and y != None and ((y[0].getpeername() == x.getpeername() and y[1].getpeername() == self._address)\
                             or (y[0].getpeername() == self._address  and y[1].getpeername() == x.getpeername())):
                            
                            try:
                                x.send(bytes(message,'utf-8'))
                                self._client.send(bytes(message,'utf-8'))
                            except Exception as e:
                                print(e)
                                continue

            print('CONNECTED PAIRS: ', len(connected_clients))


HOST = 'localhost'
PORT = 1235
ADDRESS = (HOST,PORT)
BUFSIZE = 1024
server = socket(AF_INET,SOCK_STREAM)
server.bind(ADDRESS)
server.listen(100)
sockets = []
addresses = []
connected_clients = []
active_clients = []

while True:
    print("Waiting for connection...")
    client, address = server.accept()
    print('...client connected from: ',address)
    handler = ClientHandler(client,address)
    handler.start()

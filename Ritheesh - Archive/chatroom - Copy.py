from socket import *
from codecs import decode
#from chatrecord import ChatRecord
from threading import Thread
from time import ctime

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
        if len(sockets)%2 == 0:
            connected_clients.append([sockets[-1],sockets[-2]])
        while 1:
            message = self._client.recv(BUFSIZE)
            message = message.decode('utf-8')
            # print('\n\n','Sockets = ',sockets)
            if not message:
                print("Client disconnected.")
                addIndex=sockets.index(self._client)
                del sockets[addIndex]
                del addresses[addIndex]
                for x in sockets:
                    if x in connected_clients:
                        connected_clients.remove(x)
                self._client.close()
                break
            else:
                for x in sockets:
                    # print(x.getpeername()==('127.0.0.1', int(message.split(',')[0])),x.getpeername(),('127.0.0.1',int(message.split('|')[0])))
                    if (x!=self._client and x.getpeername() == ('127.0.0.1', int(message.split('|')[0]))):
                        try:
                            if x not in connected_clients:
                                connected_clients.append(x)
                            x.send(bytes(message.split('|')[1],'utf-8'))
                        except Exception as e:
                            print(e)
                            continue
                print('CONNECTED PAIRS: ', len(connected_clients))
                # print('message : ', message)


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
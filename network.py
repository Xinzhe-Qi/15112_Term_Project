import socket
import pickle

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        hostname = socket.gethostname()    
        ipAddr = socket.gethostbyname(hostname)
        print(ipAddr)
        self.server = ipAddr
        self.port = 5556
        self.addr = (self.server, self.port)
        self.board = pickle.loads(self.connect())

    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(4096*4)
        except:
            pass

    def disconnect(self):
        self.client.close()

    def send(self, data, pick=False):
        try:
            if pick:
                self.client.send(pickle.dumps(data))
            else:
                self.client.send(str.encode(data))

            reply = self.client.recv(4096*4)

            try:
                reply = pickle.loads(reply)
            except Exception as e:
                print(e)

            return reply

        except socket.error as e:
            print(e)


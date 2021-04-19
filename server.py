import socket
from _thread import *
import pickle
from board import Board
import time

hostname = socket.gethostname()    
ipAddr = socket.gethostbyname(hostname)
print(ipAddr)

server = ipAddr
port = 5556

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    print(str(e))

s.listen(2)
print("Waiting for a connection, Server Started")

bo = Board()

currentId = "b"
connections = 0

def threaded_client(conn):
    global currentId, bo, connections

    variable = bo
    bo.start_user = currentId

    if connections > 2:
        bo.start_user = "s"

    data1 = pickle.dumps(variable)

    if currentId == "w":
        bo.ready = True
        bo.startTime = time.time()

    conn.send(data1)
    currentId = bo.start_user = "w"
    connections += 1

    while True:
        try:
            data2 = conn.recv(4096*4).decode("utf-8")

            if not data2:
                break
            else:
                if data2.count("move") > 0:
                    info = data2.split(" ")
                    x = int(info[1])
                    y = int(info[2])
                    pos = (x, y)
                    color = info[3]
                    bo.addMove(pos, color)

                elif data2 == "reset":
                    bo.__init__()

                elif data2 == "winner b":
                    bo.winner = "b"
                elif data2 == "winner w":
                    bo.winner = "w"

                print("Reveived", data2)

                if bo.ready:
                    if bo.turn == "w":
                        bo.time1 = 900 - (time.time() - bo.startTime) - bo.storedTime1
                    else:
                        bo.time2 = 900 - (time.time() - bo.startTime) - bo.storedTime2

                sendData = pickle.dumps(bo)
                print("Sending ", bo)

            conn.sendall(sendData)

        except Exception as e:
            print(e)
            break

    connections -= 1
    if connections < 2:
        bo = Board()
        currentId = "w"

    print("Disconnected")
    conn.close()


while True:
    conn, addr = s.accept()
    print("Connected to:", addr)
    start_new_thread(threaded_client, (conn,))





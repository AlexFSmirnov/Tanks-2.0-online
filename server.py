from socketserver import *
import configparser
import socket
import time
import json


class MyTCPHandler(StreamRequestHandler):
    def handle(self):    
        recv_data = self.request.recv(2 ** 15).decode("utf-8")
        command, value = json.loads(recv_data)
        if command == "get_field":
            send_data = json.dumps(field)
        else: print(recv_data)
        
        
        self.request.send(send_data.encode("utf-8"))

def loadField(path):
    floor_field = []
    walls_field = []
    ceil_field = []
    fin = open('server_files/levels/' + path)
    for i, line in enumerate(fin.readlines()):
        if i < CELLS_H:
            floor_field.append(list(line.strip())) 
        elif i < 2 * CELLS_H:
            walls_field.append(list(line.strip())) 
        else:
            ceil_field.append(list(line.strip())) 
    fin.close()
    return [floor_field, walls_field, ceil_field]


#CONFIG------------------------------------------------------------------------#
config = configparser.ConfigParser()
config.read('server_files/config.ini')

CELLS_W = int(config['DISPLAY SIZE']['CELLS_W'])
CELLS_H = int(config['DISPLAY SIZE']['CELLS_H'])
#---#
      
host = socket.gethostbyname(socket.gethostname())
port = 25567
addr = (host, port)

field = loadField("test_level.txt")

server = TCPServer(addr, MyTCPHandler)
print("Starting server on {}:{}".format(host, port))

server.serve_forever()
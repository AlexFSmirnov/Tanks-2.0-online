from twisted.internet import protocol, reactor, task
from pygame import *
import pygame
import entities
import json
import socket


class TwistServer(protocol.Protocol):
    def __init__(self):
        self.users = []
        self.field = self.
               
    def connectionMade(self):
        print( 'connection success!')
        self.users.append(self)

    def dataReceived(self, data):
        print(data.decode("utf-8"))
        
        self.transport.write(b'Hello from server!')

    def connectionLost(self, reason):
        print('Connection lost!', reason)
    

host = socket.gethostbyname(socket.gethostname())
port = 25565
factory = protocol.Factory()
factory.protocol = TwistServer
print("Starting server on {}:{}".format(host, port))
reactor.listenTCP(port, factory)
reactor.run()

import pygame
from pygame import *
from twisted.internet import protocol, reactor

class Twist_client(protocol.Protocol):
    #Отправка сообщения с проверкой
    def sendString(self, string):
        self.transport.write(string.encode("utf-8"))
    
    def connectionMade(self):
        print("Successfully connected to {}:{}".format(host, port))
        
    def dataReceived(self, data):
        print(data)
        
class Twist_Factory(protocol.ClientFactory):
    protocol = Twist_client
    
    def clientConnectionFailed(self, connector, reason):
        print('connection failed:', reason.getErrorMessage())
        reactor.stop()

    def clientConnectionLost(self, connector, reason):
        print('connection lost:', reason.getErrorMessage())
        reactor.stop()
        
        
host = input("Server IP: ")
port = int(input("Server port: "))
factory = Twist_Factory()
reactor.connectTCP(host, port, factory)
reactor.run()
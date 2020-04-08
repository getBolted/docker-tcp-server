#Модуль socketserver для сетевого программирования
from socketserver import *
import urllib.request
import json
import requests
import socket 
#данные сервера
host = '0.0.0.0'
port = 32000
addr = (host,port)

#обработчик запросов TCP подкласс StreamRequestHandler
class MyTCPHandler(StreamRequestHandler):
    response  = 'Pod {0} got message: '.format(socket.gethostname())
    #функция handle делает всю работу, необходимую для обслуживания запроса. 
    #доступны несколько атрибутов: запрос доступен как self.request, адрес как self.client_address, экземпляр сервера как self.server
    def handle(self):     
        self.data = self.request.recv(1024)
        print ('client sent: '+str(self.data))
        self.response += self.data.decode('utf-8')
        #sndall - отправляет сообщение
        self.request.sendall(bytes(self.response, 'utf-8'))

if __name__ == "__main__":
    
    #Создаем экземпляр класса
    server = TCPServer(addr, MyTCPHandler)
    print('starting server... for exit press Ctrl+C')
    #serve_forever - запускаем сервер
    server.serve_forever()
from datetime import datetime

class bufferData():                         # Objeto valor do dicionario. Precisamos da hora de entrada na cache    
    def __init__(self, time, data):
        self.time = hora
        self.data  = data

    def getHora():
        return self.hora

    def getData():
        return self.data

class cache():
    def __init__ (self, size):
        self.buffer = {}                        # Dicionario representando a cache. Tem como valor uma instancia da classe bufferData
        self.size = size                        # Capacidade total
        self.currentCapacity = size             # Espaco disponivel

    def addToCache(url, dictData):
        if (len(data) <= currentCapacity):
            self.buffer[url] = dictData
            self.currentCapacity -= len(dictData.getData())
        else:
            max = 0
            elem = ''

            while (len(data) <= currentCapacity):

                for e in self.buffer:
                    if self.buffer[e].getHora() > max:
                        max = self.buffer[e].getHora()
                        elem = e

                del(self.buffer[elem])

            self.buffer[url] = dictData
            self.currentCapacity -= len(dictData.getData())

    def removeFromCache(url):
        if url in self.cache:
            self.currentCapacity += len(self.cache[url].getData())
            del(self.cache[url])
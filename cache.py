from datetime import datetime

class bufferData():                         # Objeto valor do dicionario. Precisamos da hora de entrada na cache    
    def __init__(self, time, data):
        self.time = time                    # Hora de entrada na cache
        self.data  = data                   # Dados de resposta

    def getHora():
        return self.hora

    def getData():
        return self.data

class cache():
    def __init__ (self):
        self.buffer = {}                            # Dicionario representando a cache. Tem como valor uma instancia da classe bufferData
        self.size = 20000000                        # Capacidade total medida em bytes
        self.currentCapacity = 20000000             # Espaco disponivel atual

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
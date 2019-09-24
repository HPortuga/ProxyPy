class BufferData():                         # Objeto valor do dicionario. Precisamos da hora de entrada na cache    
    def __init__(self, time, data):
        self.time = time                    # Hora de entrada na cache
        self.data  = data                   # Dados de resposta

    def getHora(self):
        return self.time

    def getData(self):
        return self.data

class Cache():
    def __init__ (self):
        self.buffer = {}                            # Dicionario representando a cache. Tem como chave a url e como valor uma instancia da classe bufferData
        self.size = 20000000                        # Capacidade total medida em bytes
        self.currentCapacity = 20000000             # Espaco disponivel atual

    def addToCache(self, url, dictData):                  # dicData eh instancia de bufferData
        if (len(dictData.getData()) <= self.currentCapacity):
            self.buffer[url] = dictData
            self.currentCapacity -= len(dictData.getData())
        else:
            max = 0
            elem = ''

            while (len(dictData.getData()) <= self.currentCapacity):

                for e in self.buffer:
                    if self.buffer[e].getHora() > max:
                        max = self.buffer[e].getHora()
                        elem = e

                del(self.buffer[elem])

            self.buffer[url] = dictData
            self.currentCapacity -= len(dictData.getData())

    def removeFromCache(self, url):
        if url in self.buffer:
            self.currentCapacity += len(self.buffer[url].getData())
            del(self.buffer[url])
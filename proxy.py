import socket
import _thread
import sys
import datetime
from cache import Cache

LOG = "log.txt"

class ProxyServer():
   def __init__ (self, porta, blacklist, cache):
      self.porta = porta
      self.blacklist = blacklist
      self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      self.sock.bind(('', self.porta))
      self.inicializarLog()
      self.cache = cache

   def inicializarLog(self):
      self.log = open(LOG, "w")     # w cria ficheiro caso nao exista e sobrescreve caso exista (apaga o conteudo)
      self.log.write("Proxy Iniciado em: localhost - %d" % self.porta)
      self.log.write("\n")
      self.log.write("Server Time: %s" % datetime.datetime.now())
      self.log.write("\n")
      self.log.write("------------------------------------------------------")
      self.log.write("\n")
      self.log.write("\n")
      self.log.close()

   def escreverNoLog(self, string):
      self.log = open(LOG, "a")     # Apende texto no final do arquivo
      self.log.write(string)
      self.log.write("\n")
      self.log.close()

   def escutar(self):
      self.sock.listen(50)

      while True:
         clientSocket, endereco = self.sock.accept()
         self.escreverNoLog("Conexao com %s foi estabelecida!" % str(tuple(endereco)))

         _thread.start_new_thread(self.executarProxy, (clientSocket, endereco, self.blacklist))

      self.sock.close()

   def executarProxy(self, clientSocket, endereco, blacklist):
      # Requisicao do servidor
      data = clientSocket.recv(999999)
      request = str(data)

      if (request == ""):
         self.escreverNoLog("Requisicao Invalida! Fechando socket com cliente...")
         clientSocket.close()
         sys.exit(1)

      # Parse request
      first_line = request.split('\n')[0]
      url = first_line.split(' ')[1]
      connectionMethod = first_line.split(' ')[0].replace("b'", "")

      if (connectionMethod == "GET" or connectionMethod == "CONNECT"):
         webserver, port = self.getAddress(url)

         # Procurar se url esta na blacklist
         if (webserver in blacklist):
            self.escreverNoLog("%s esta na blacklist!" % webserver)
            clientSocket.close()
            sys.exit(1)

            # Verificar se a requisição está na cache (usar dicionário onde url é a chave e os dados são o valor)
            # else if url in cache:
               # TODO
            # É necessário ir buscar no servidor
            
            # Enviar resposta ao browser
            serverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            serverSock.connect((webserver, port))

            try:
               serverSock.send(data)               # Envia a requisição ao servidor
            except socket.error as ex:
               print (ex)

            while True:                         # Recebe a resposta em "pedaços" de 8192 bytes
               reply = serverSock.recv(999999)
               if len(reply) > 0:
                  clientSocket.send(reply)      # Ta enviando "b''"
               else:
                  break

            serverSock.close()
            clientSocket.close()

      else:
         self.escreverNoLog("SERVER ERROR - NOT IMPLEMENTED (502): %s" % connectionMethod)
         clientSocket.close()
         sys.exit(1)

   def enviarResposta(self, url, clientSocket, data):
      # Cria socket para comunicação com o servidor
      webserver, port = self.getAddress(url)
      serverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      serverSock.connect((webserver, port))

      try:
         serverSock.send(data)               # Envia a requisição ao servidor
      except socket.error as ex:
         print (ex)

      while True:                         # Recebe a resposta em "pedaços" de 8192 bytes
         reply = serverSock.recv(999999)
         if len(reply) > 0:
            clientSocket.send(reply)
         else:
            break

      serverSock.close()
      clientSocket.close()
   
   def getWebserver(self, url):
      # Remover http:// se existir
      httpPos = url.find("://")
      if (httpPos == -1):
         webserver = url
      else:
         webserver = url[(httpPos + 3):]

      # Remover caminho do servidor se existir (google.com/fotos)
      webserverEnd = webserver.find("/")
      if (webserverEnd == -1):
         webserverEnd = len(webserver)

      return webserver[:webserverEnd]

   def getPort(self, url):
      portBegin = url.find(":")

      port = -1
      if (portBegin == -1):
         port = 80
      else:
         temp = url[portBegin + 1:]
         port = int(temp)
      
      return port

   def getAddress(self, url):
      webserver = self.getWebserver(url)
      port = self.getPort(webserver)

      portString = ":" + str(port)

      webserver = webserver.replace(portString, "")

      return (webserver, port)     

def atribuirPorta():
   if (len(sys.argv) >= 2):
      argumentos = sys.argv[1]
      nomeArg = argumentos[:3]

      if (nomeArg == '-p='): 
         porta = argumentos
         porta = int(porta[-4:])
         return porta
   
   print("Nenhuma porta selecionada. Escolhendo :8080")
   return 8080

if __name__ == "__main__":
   arq = open(sys.argv[2], 'r')
   blacklist = arq.readlines()
   porta = atribuirPorta()
   cache = Cache()
   proxyServer = ProxyServer(porta, blacklist, cache)
   proxyServer.escutar()
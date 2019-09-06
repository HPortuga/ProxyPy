import socket
import sys

class ProxyServer():
   def __init__ (self, port):
      self.port = port
      self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      self.sock.bind((socket.gethostname(), self.port))

   def escutar(self):
      print("escutando...")
      self.sock.listen(5)

      while True:
         (clientsocket, endereco) = self.sock.accept()
         print("Conexao com " + str(tuple(endereco)) + " foi estabelecida!")

if __name__ == "__main__":
   argumentos = sys.argv[1]
   nomeArg = argumentos[:3]
   if (nomeArg == '-p='): 
      porta = argumentos
      porta = int(porta[-4:])

   proxyServer = ProxyServer(porta)
   proxyServer.escutar()

   
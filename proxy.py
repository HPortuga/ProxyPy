import socket
import _thread
import sys

class ProxyServer():
   def __init__ (self, porta):
      self.porta = porta
      self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      self.sock.bind(('', self.porta))

   def escutar(self):
      print("Escutando na porta ", porta ,"...")
      self.sock.listen(50)

      while True:
         clientSocket, endereco = self.sock.accept()
         print("Conexao com " + str(tuple(endereco)) + " foi estabelecida!")

         # Essa e a funcao que deve ser executada dentro da thrad
         _thread.start_new_thread(self.executarProxy, (clientSocket, endereco))

      self.sock.close()

   def executarProxy(self, clientSocket, endereco):
      # Requisicao do Browser
      request = clientSocket.recv(999999)

      # Procurar se url esta na blacklist

      # Procurar na cache

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
   porta = atribuirPorta()
   proxyServer = ProxyServer(porta)
   proxyServer.escutar()

   
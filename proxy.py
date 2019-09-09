import socket
import _thread
import sys

class ProxyServer():
   def __init__ (self, porta, blacklist):
      self.porta = porta
      self.blacklist = blacklist
      self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      self.sock.bind(('', self.porta))

   def escutar(self):
      print("Escutando na porta ", porta ,"...")
      self.sock.listen(50)

      while True:
         clientSocket, endereco = self.sock.accept()
         print("Conexao com " + str(tuple(endereco)) + " foi estabelecida!")

         # Essa e a funcao que deve ser executada dentro da thrad
         _thread.start_new_thread(self.executarProxy, (clientSocket, endereco, self.blacklist))

      self.sock.close()

   def executarProxy(self, clientSocket, endereco, blacklist):

      # Requisicao do Browser
      request = str(clientSocket.recv(999999))

       # Pega primeira linha do pedido
      first_line = request.split('\n')[0]

      # pega a url
      url = first_line.split(' ')[1].replace(':443', '')

      print("\nURL: " + url + "\n")


      # Procurar se url esta na blacklist
      if (url in blacklist):
         print("URL na blacklist!")
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
   arq = open(sys.argv[2], 'r')
   blacklist = arq.readline()
   porta = atribuirPorta()
   proxyServer = ProxyServer(porta, blacklist)
   proxyServer.escutar()

   
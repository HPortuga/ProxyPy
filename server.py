import socket
import _thread
import sys

class ProxyServer():
   def __init__ (self, porta):
      self.porta = porta
      self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      self.sock.bind((socket.gethostname(), self.porta))

   def escutar(self):
      print("Escutando na porta ", porta ,"...")
      self.sock.listen(50)

      while True:
         clientSocket, endereco = self.sock.accept()
         print("Conexao com " + str(tuple(endereco)) + " foi estabelecida!")

         # Essa e a funcao que deve ser executada dentro da thrad
         _thread.start_new_thread(executarThread, (clientSocket, endereco))

      self.sock.close()

def executarThread(clientSocket, endereco):
   # Requisicao do Browser
   request = clientSocket.recv(999999)

   linha = request.split("\n")[0]
   url = linha.split(' ')[1]

   print("Request ", linha, endereco)

   # Procurar se url esta na blacklist

   # Procurar na cache

   # Encontrar webserver e porta
   http_pos = url.find("://")          
   if (http_pos==-1):
      temp = url
   else:
      temp = url[(http_pos+3):]       
    
   port_pos = temp.find(":")           

   webserver_pos = temp.find("/")
   if webserver_pos == -1:
      webserver_pos = len(temp)

   webserver = ""
   port = -1
   if (port_pos==-1 or webserver_pos < port_pos):      
      port = 80
      webserver = temp[:webserver_pos]
   else:       
      port = int((temp[(port_pos+1):])[:webserver_pos-port_pos-1])
      webserver = temp[:port_pos]

   s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
   s.connect((webserver, port))
   s.send(request)         
   
   while 1:
      data = s.recv(999999)
      
      if (len(data) > 0):
         # send to browser
         clientSocket.send(data)
      else:
         break
   s.close()
   clientSocket.close()


def atribuirPorta():
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

   
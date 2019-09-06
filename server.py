import sys

class SocketServer():
   def __init__ (self, port):
      self.port = port

if __name__ == "__main__":
   argumento = sys.argv[1]
   ha = ""

   nomeArg = argumento[:3]
   if (nomeArg == '-p='): 
      porta = argumento
      ha = porta[2:6]

   print ("The arguments are: " , ha)
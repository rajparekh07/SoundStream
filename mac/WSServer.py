from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
import base64

class WSServer(WebSocket):

    def handleMessage(self):

       inst = self.data.split(":")[0]
       args = self.data.split(":")[1]

       try:
          if inst == "INST" :
            WSServer.onMessageCallbacks[args]()
          else :
            WSServer.onMessageCallbacks[inst](args)
       except Exception as e:
          print(e)
      

       for client in clients:
          if client != self:
             client.sendMessage(self.address[0] + u' - ' + self.data)
    clients = []
    onConnectionCallbacks = []
    onMessageCallbacks = {}

    @classmethod
    def bindOnConnection(cls, func):
        WSServer.onConnectionCallbacks.append(func)

    @classmethod
    def on(cls, event, func):
        WSServer.onMessageCallbacks[event] = func

    @classmethod
    def send(cls, d):
        # print(cls.clients)
        for client in cls.clients:
            client.sendMessage(d)
            # client.sendMessage(base64.b64encode(d))

    def handleConnected(self):
       print(self.address, 'connected')
       
       # for client in WSServer.clients:
          # client.sendMessage(self.address[0] + u' - connected')    
          
       WSServer.clients.append(self)
       for c in WSServer.onConnectionCallbacks:
            c()
       print(WSServer.clients)

    def handleClose(self):
       WSServer.clients.remove(self)
       print(self.address, 'closed')
       for client in WSServer.clients:
          client.sendMessage(self.address[0] + u' - disconnected')

if __name__ == '__main__':
  server = SimpleWebSocketServer('', 8000, WSServer)
  server.serveforever()
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5 import QtWebSockets

class WebSocketHandler(QObject):
    message_received = pyqtSignal(str)

    def __init__(self):
        super(QObject,self).__init__()
        self.server = QtWebSockets.QWebSocketServer("WebSocket Server", QtWebSockets.QWebSocketServer.NonSecureMode)
        self.server.newConnection.connect(self.on_new_connection)
        self.clients = []

    def on_new_connection(self):
        socket = self.server.nextPendingConnection()
        socket.textMessageReceived.connect(self.on_text_message_received)
        socket.disconnected.connect(self.on_disconnected)
        self.clients.append(socket)

    def on_text_message_received(self, message):
        self.message_received.emit(message)

    def on_disconnected(self):
        socket = self.sender()
        self.clients.remove(socket)
        socket.deleteLater()

    def broadcast(self, message):
        c=0
        for client in self.clients:
            client.sendTextMessage(message)
            print("cliente",c)
            c=c+1
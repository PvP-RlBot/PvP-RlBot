from socket import socket
from typing import Callable

import eventlet
import socketio
from eventlet import wsgi


class Server:
    """
    Use this Server class to easily listen to connections on a specific host and port.
    """
    def __init__(self):
        self.sio = socketio.Server()
        self.app = socketio.WSGIApp(self.sio)
        self.socket: socket = None
        self.__clients = []

        @self.sio.event
        def connect(sid, environ, auth):
            self.__clients.append(sid)

        @self.sio.event
        def disconnect(sid):
            self.__clients.remove(sid)

    def start(self, host='', port=5000):
        self.socket = eventlet.listen((host, port))
        wsgi.server(self.socket, self.app)

    def stop(self):
        try:
            self.socket.close()
        except Exception:
            pass

    def set_reception_callback(self, callback: Callable[[str], None]):
        @self.sio.on('*')
        def catch_all(event, data):
            callback(data)

    def amount_of_connections(self):
        return len(self.__clients)

    def get_sids(self):
        return self.__clients

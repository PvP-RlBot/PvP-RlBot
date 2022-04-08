from typing import Callable

import eventlet
import socketio

sio = socketio.Server()
app = socketio.WSGIApp(sio)


class Server:
    """
    Use this Server class to easily listen to connections on a specific host and port.
    """
    def __init__(self):
        self.sio = socketio.Server()
        self.app = socketio.WSGIApp(sio)
        self.__clients = []

        @sio.event
        def connect(sid, environ, auth):
            self.__clients.append(sid)

        @sio.event
        def disconnect(sid):
            self.__clients.remove(sid)

    def start(self, host='', port=5000):
        eventlet.wsgi.server(eventlet.listen((host, port)), app)

    def set_reception_callback(self, callback: Callable[[str], None]):
        @sio.on('*')
        def catch_all(event, data):
            callback(data)

    def amount_of_connections(self):
        return len(self.__clients)

    def get_sids(self):
        return self.__clients

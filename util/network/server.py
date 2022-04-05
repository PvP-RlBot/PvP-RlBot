from typing import Callable

import eventlet
import socketio

sio = socketio.Server()
app = socketio.WSGIApp(sio)


class ServerUtils:
    """
    This class is for implementing a basic server connection.
    If you're just interested in listening to incoming connections on a certain host and port,
    you should use the Server class instead.
    """
    __clients = []
    __reception_callback: Callable[[str], None] = lambda s: None

    @staticmethod
    def start(host='', port=5000):
        eventlet.wsgi.server(eventlet.listen((host, port)), app)

    @staticmethod
    def receive_connection(sid):
        ServerUtils.__clients.append(sid)

    @staticmethod
    def terminate_connection(sid):
        ServerUtils.__clients.remove(sid)

    @staticmethod
    def receive_data(str_data):
        ServerUtils.__reception_callback(str_data)

    @staticmethod
    def set_reception_callback(callback: Callable[[str], None]):
        ServerUtils.__reception_callback = callback

    @staticmethod
    def amount_of_connections():
        return len(ServerUtils.__clients)


class Server:
    """
    Use this Server class to easily listen to connections on a specific host and port.
    """
    @staticmethod
    def start(host='', port=5000):
        ServerUtils.start(host, port)

    @staticmethod
    def set_reception_callback(callback: Callable[[str], None]):
        ServerUtils.set_reception_callback(callback)

    @staticmethod
    def amount_of_connections():
        return ServerUtils.amount_of_connections()


@sio.event
def connect(sid, environ):
    ServerUtils.receive_connection(sid)


@sio.on('*')
def catch_all(event, data):
    ServerUtils.receive_data(data)


@sio.event
def disconnect(sid):
    ServerUtils.terminate_connection(sid)

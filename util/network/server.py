import eventlet
import socketio

sio = socketio.Server()
app = socketio.WSGIApp(sio)


class Server:
    __clients = []

    @staticmethod
    def start(host='', port=5000):
        eventlet.wsgi.server(eventlet.listen((host, port)), app)

    @staticmethod
    def receive_connection(sid):
        Server.__clients.append(sid)

    @staticmethod
    def terminate_connection(sid):
        Server.__clients.remove(sid)

    @staticmethod
    def receive_data(str_data):
        sio.emit('*', data=str_data)

    @staticmethod
    def amount_of_connections():
        return len(Server.__clients)


@sio.event
def connect(sid, environ):
    Server.receive_connection(sid)


@sio.on('*')
def catch_all(event, data):
    Server.receive_data(data)


@sio.event
def disconnect(sid):
    Server.terminate_connection(sid)

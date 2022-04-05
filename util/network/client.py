import socketio

sio = socketio.Client()


class ClientUtils:
    __is_connected = False

    @staticmethod
    def start(url):
        sio.connect(url, wait=False)

    @staticmethod
    def got_connected():
        ClientUtils.__is_connected = True

    @staticmethod
    def got_disconnected():
        ClientUtils.__is_connected = False

    @staticmethod
    def send_data(str_data):
        sio.emit('*', data=str_data)

    @staticmethod
    def is_connected():
        return ClientUtils.__is_connected


class Client:
    @staticmethod
    def start(url='http://localhost:5000'):
        ClientUtils.start(url)

    @staticmethod
    def send_data(str_data):
        ClientUtils.send_data(str_data)

    @staticmethod
    def is_connected():
        return ClientUtils.is_connected()


@sio.event
def connect():
    ClientUtils.got_connected()


@sio.event
def disconnect():
    ClientUtils.got_disconnected()

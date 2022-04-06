import socketio

sio = socketio.Client()


class ClientUtils:
    """
    This class is for implementing a basic client connection.
    If you're just interested in establishing a connection to a server using a certain url,
    you should use the Client class instead.
    """
    __is_connected = False

    @staticmethod
    def start(url):
        sio.connect(url)

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
    """
    Use this Client class to easily connect to a server on a specific url.
    """
    @staticmethod
    def start(url='http://localhost:5000'):
        ClientUtils.start(url)

    @staticmethod
    def send_data(str_data):
        ClientUtils.send_data(str_data)

    @staticmethod
    def is_connected():
        return ClientUtils.is_connected()

    @staticmethod
    def get_sid():
        return sio.get_sid()


@sio.event
def connect():
    ClientUtils.got_connected()


@sio.event
def disconnect():
    ClientUtils.got_disconnected()

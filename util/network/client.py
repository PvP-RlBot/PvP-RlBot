import socketio


class Client:
    """
    Use this Client class to easily connect to a server on a specific url.
    """
    def __init__(self):
        self.sio = socketio.Client()

    def start(self, url='http://localhost:5000'):
        try:
            self.sio.connect(url)
        except ConnectionError:
            pass

    def stop(self):
        self.sio.disconnect()

    def send_data(self, str_data):
        self.sio.emit('*', data=str_data)

    def is_connected(self):
        return self.sio.connected

    def get_sid(self):
        return self.sio.get_sid()

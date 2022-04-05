import socketio

sio = socketio.Client(reconnection=False)


class Client:
    __is_connected = False

    @staticmethod
    def start(url='http://localhost:5000'):
        sio.connect(url)

    @staticmethod
    def stop():
        if Client.__is_connected:
            return
        sio.disconnect()

    @staticmethod
    def got_connected():
        Client.__is_connected = True

    @staticmethod
    def got_disconnected():
        Client.__is_connected = False

    @staticmethod
    def send_data(str_data):
        sio.emit('*', data=str_data)

    @staticmethod
    def is_connected():
        return Client.__is_connected


@sio.event
def connect():
    print("con")
    Client.got_connected()


@sio.event
def disconnect():
    print("dis")
    Client.got_disconnected()

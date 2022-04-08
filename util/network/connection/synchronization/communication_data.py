from util.io.game_state import GameState


class CommunicationData:
    def __init__(self, url, host, port):
        self.received_sync_data = None
        self.url = url
        self.host = host
        self.port = port

    def receiveSyncData(self, data: str):
        self.received_sync_data = GameState.fromJSON(data)


class CommunicationDataBuilder:
    def __init__(self):
        self.__url = None
        self.__host = None
        self.__port = None

    def withURL(self, url):
        self.__url = url
        return self

    def withHost(self, host):
        self.__host = host
        return self

    def withPort(self, port):
        self.__port = port
        return self

    def build(self):
        return CommunicationData(self.__url, self.__host, self.__port)

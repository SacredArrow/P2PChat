from multiprocessing import Queue
from enum import Enum, auto


class MessageType(Enum):
    CLIENT_CLOSED = auto()
    SERVER_CLOSED = auto()
    CLIENT_MESSAGE = auto()
    CONNECTION_ERROR = auto()


class Message:
    """
    Data type which is used to transfer messages through the MessageBus.
    """

    type: MessageType = None
    text = None

    def __init__(self, msg_text, msg_type):
        self.text = msg_text
        self.type = msg_type


class MessageBus:
    """
    Publisher responsible for message exchange between UserInterface and Server.
    """

    _queues = None
    _themes = None

    def __init__(self):
        self._queues = dict()
        self._themes = dict()

    def subscribe(self, subscriber, themes):
        if subscriber not in self._queues.keys():
            self._queues.update({subscriber: Queue()})

        for theme in themes:
            if theme not in self._themes.keys():
                self._themes.update({theme: [subscriber]})
            else:
                self._themes[theme].append(subscriber)

    def send_message(self, message, theme):
        if theme in self._themes.keys():
            for subscriber in self._themes[theme]:
                self._queues[subscriber].put(message)

    def get_messages(self, subscriber):
        while self._queues[subscriber].qsize():
            yield self._queues[subscriber].get()

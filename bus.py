from multiprocessing import Queue

class MessageBus:
    incoming_messages = None
    outcoming_messages = None
    def __init__(self):
        self.incoming_messages = Queue()
        self.outcoming_messages = Queue()


from connector import Connector


class RippleClient(Connector):
    id = "RippleClient"
    
    def __init__(self, pairs, depth=None, command='book_offers'):
        super().__init__(pairs, depth, command)
        self.url = 'wss://s1.ripple.com/'
        self.payload = {"id": self.id, "command": command, "taker": "r9cZA1mLK5R5Am25ArfXFmqgNwjZgnfk59"}
        
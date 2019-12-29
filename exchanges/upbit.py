
from connector import Connector
from constants import UPBIT

import threading

class Upbit(Connector):
    
    id = UPBIT
    
    def __init__(self, pairs, depth=None, **kwargs):
        super().__init__(pairs, depth, **kwargs)
        self.url = 'wss://api.upbit.com/websocket/v1'
        self.format_pairs = '{}-{}'.format(self.quote.upper(), self.base.upper())
        self.payload = [{"ticket":"%s" % self.id}, 
                        {"type": "orderbook", 
                         "codes": ["%s" % self.format_pairs],
                         "isOnlyRealtime": True}]
        
    def on_data(self, data, data_type, flag):
        data = super().on_data(data, data_type, flag)
        self.zsock.send_pyobj(self.handler(data))
        self.zsock.recv()
        
    def handler(self, message):
        """
        Response Example
        [
            {
                "ask_price": ...
                "ask_size": ...
                "bid_price": ...
                "bid_size": ...
            },
            {
                "ask_price": ...
                "ask_size": ...
                "bid_price": ...
                "bid_size": ...
            },
        ]
        """
        message = message['orderbook_units'][0]
        asks = [message['ask_price'], message['ask_size']]
        bids = [message['bid_price'], message['bid_size']]
        
        return message
    

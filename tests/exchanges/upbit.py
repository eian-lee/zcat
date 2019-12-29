
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
        self.zsock.send_json(self.message_handler(data))
        self.zsock.recv()
        
    def message_handler(self, message):
        """
        NOTE
        : 업비트는 인덱스로 먼저 접근한 뒤, ask/bid 가격과 수량을 딕셔너리 key로 접근
        : 그래서 깊이설정이 어려움
        OrderBook
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
        
        # depth 적용하기 어려움, list comprehension으로 처리해야 할듯
        asks = [message['ask_price'], message['ask_size']]
        bids = [message['bid_price'], message['bid_size']]
        
        return self.convert(name=self.name,
                            asks=[asks],
                            bids=[bids],
                            timestamp=self.nonce())
    
    

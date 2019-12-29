
from itertools import islice
from connector import Connector
from defines import ASK, BID, PRICE, SIZE, KRAKEN
from tools.parallel import update_asks_bids

class Kraken(Connector):
    
    id = KRAKEN
    
    def __init__(self, pairs, depth, **kwargs):
        super().__init__(pairs, depth, **kwargs)
        self.format_pairs = f"{self.base.upper()}/{self.quote.upper()}"
        self.url = 'wss://ws.kraken.com'
        self.payload = {'event': 'subscribe',
                        'pair': [f"{self.format_pairs}"],
                        'subscription': {'name': 'book'}}
        
        # 오더북 설정
        self.orderbook = {}
        
    def on_data(self, data, data_type, flag):
        data = super().on_data(data, data_type, flag)
        self.zsock.send_pyobj(self.handler(data))
        self.zsock.recv()
    
    def handler(self, message: list):
        message = message[1:-2]
        # 스냅샷 저장
        if 'as' in message[0]:
            self.orderbook = {'name': self.name,
                              'asks': {x[PRICE]: x[SIZE] for x in message[0]['as']},
                              'bids': {x[PRICE]: x[SIZE] for x in message[0]['bs']}}
            return self.orderbook
        
        # 1. ASK | BID
        for msg in message:
            for key, value in msg.items():
                side = ASK if key == 'a' else BID
                for price, size, *_ in value:
                    if price in self.orderbook[side]:
                        if float(size) == 0:
                            del self.orderbook[side][price]
                    if float(size) != 0:
                        self.orderbook[side].update({price: size})
                        self.orderbook[side] = dict(islice(sorted(self.orderbook[side].items()), self.depth))
                        
        # 2. ASK & BID
        if len(message) != 1:
            a, b = message
            asks, bids = update_asks_bids(a, b)
            for index, orders in enumerate((asks, bids)):
                # 주문타입 판단(0번째 인덱스는 반드시 ASK임)
                side = ASK if index == 0 else BID
                for price, size in orders:
                    if price in self.orderbook[side].keys():
                        if float(size) == 0:
                            del self.orderbook[side][price]
                    if float(size) != 0:
                        self.orderbook[side].update({price: size})
                        self.orderbook[side] = dict(islice(sorted(self.orderbook[side].items()), self.depth))
        return self.orderbook

from itertools import islice
from connector import Connector
from defines import ASK, BID, BITFINEX


class Bitfinex(Connector):
    
    id = BITFINEX
    
    def __init__(self, pairs, depth=None, **kwargs):
        super().__init__(pairs, depth, **kwargs)
        self.format_pairs = "t{}{}".format(self.base.upper(), self.quote.upper())
        self.url = 'wss://api-pub.bitfinex.com/ws/2'
        self.payload = {"event": "subscribe",
                        "channel": "book",
                        "symbol": "tBTCUSD",
                        "prec": "P0",
                        "freq": "F0",
                        "len": 25}
        # 오더북 설정
        self._book = {}
        
    def on_data(self, data, data_type, flag):
        data = super().on_data(data, data_type, flag)
        self.zsock.send_pyobj(self.handler(data))
        self.zsock.recv()
        
    def handler(self, message):
        message = message[1]
        # print(message)
        if type(message) is list:
            if len(message) != 3:
                self._book = {'name': self.name,
                              'bids': {x[0]: x[-1] for x in message[:25]},
                              'asks': {x[0]: abs(x[-1]) for x in message[25:]}}
                return self._book
            price, count, size = message
            if count != 0:
                side = BID if size > 0 else ASK
                if price in self._book[side]:
                    self._book[side].update({price: abs(size)})
                    return self._book
                self._book[side].update({price: abs(size)})
                self._book[side] = dict(islice(sorted(self._book[side].items()), 25))
                return self._book
            if count == 0:
                side = BID if size == 1 else ASK
                del self._book[side][price]
                return self._book
from connector import Connector
from timer import timer
from pprint import pprint

class Kraken(Connector):
    
    order_book = None
    
    def __init__(self, pairs, depth=None, **kwargs):
        super().__init__(pairs, depth, **kwargs)
        self.format_pairs = '{}/{}'.format(self.base.upper(), self.quote.upper())
        self.url = 'wss://ws.kraken.com'
        self.payload = {'event': 'subscribe',
                        'pair': ['%s' % self.format_pairs],
                        'subscription': {'name': 'book'}}
    
    def on_data(self, data, data_type, flag=1):
        data = super().on_data(data, data_type, flag)
        self.zsock.send_json(self.message_handler(data))
        # self.zsock.send_json(data)
        self.zsock.recv()
    
    @timer
    def message_handler(self, message: list):
        message = message[1:-2]
        # 스냅샷 저장
        if 'as' in message[0]:
            self.order_book = self.convert(bids=message[0]['bs'][:self.depth],
                                           asks=message[0]['as'][:self.depth])
        # 업데이트
        else:
            for msg in message:
                for key, value in msg.items():
                    side = 'bids' if key == 'b' else 'asks'
                    for index, orders in enumerate(value):
                        price = float(orders[0])
                        size = float(orders[1])
                        print("Side: %s, Price: %f" % (side, price))
                        if size == 0:
                            if float(self.order_book['bids'][-1][0]) < price < float(self.order_book['asks'][-1][0]):
                                for idx, target in enumerate(self.order_book[side]):
                                    if price == float(target[0]):
                                        self.order_book[side].pop(idx)
                        else:
                            for idx, target in enumerate(self.order_book[side]):
                                if price == float(target[0]):
                                    del self.order_book[side][idx]
                    self.order_book[side].append(orders)
        self.order_book['bids'].sort(key=lambda element: element[0], reverse=True)
        self.order_book['asks'].sort(key=lambda element: element[0])
        
        result = {
            'name': self.name,
            'bids': self.order_book['bids'][:self.depth],
            'asks': self.order_book['asks'][:self.depth]
        }
        return result
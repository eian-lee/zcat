
from decimal import Decimal
from connector import Connector


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
        data, recv_at = super().on_data(data, data_type, flag)
        self.zsock.send_json(self.message_handler(data))
        self.zsock.recv()
    
    def message_handler(self, message: list):
        message = message[1:-2]
        # 스냅샷 저장
        if 'as' in message[0]:
            self.order_book = self.convert(bids=message[0]['bs'],
                                           asks=message[0]['as'])
        # 업데이트
        else:
            for msg in message:
                for key, value in msg.items():
                    side = 'bids' if key == 'b' else 'asks'
                    for index, orders in enumerate(value):
                        price = float(orders[0])
                        size = float(orders[1])
                        if size == 0:
                            for idx, target in enumerate(self.order_book[side]):
                                if price == float(target[0]):
                                    self.order_book[side].pop(idx)
                        else:
                            for idx, target in enumerate(self.order_book[side]):
                                if price == float(target[0]):
                                    del self.order_book[side][idx]
                    self.order_book[side].append(orders)
        result = {'name': self.name, 
                  'asks': sorted(self.order_book['asks'], key=lambda x: x[0]),
                  'bids': sorted(self.order_book['bids'], key=lambda x: x[0], reverse=True)}
        return result
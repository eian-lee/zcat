
from connector import Connector
from collections import OrderedDict as od
from defines import UPBIT, ASK, BID

AP, AS = 'ask_price', 'ask_size'
BP, BS = 'bid_price', 'bid_size'


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
        self._book = {}
        
    def on_data(self, data, data_type, flag):
        data = super().on_data(data, data_type, flag)
        self.zsock.send_pyobj(self.handler(data))
        # self.zsock.send_pyobj(data)
        self.zsock.recv()
        
    def handler(self, message):
        """
        업비트 응답예제
        {'code': 'KRW-BTC',
        'orderbook_units': [{'ask_price': 8563000.0,
                            'ask_size': 0.06914287,
                            'bid_price': 8556000.0,
                            'bid_size': 0.08541616},
                            {'ask_price': 8564000.0,
                            'ask_size': 0.26,
                            'bid_price': 8555000.0,
                            'bid_size': 0.67899999},
                            {'ask_price': 8565000.0,
                            'ask_size': 0.5837,
                            'bid_price': 8551000.0,
                            'bid_size': 0.3296},
                            {'ask_price': 8566000.0,
                            'ask_size': 1.9676461,
                            'bid_price': 8550000.0,
                            'bid_size': 0.14940003000000002},
                            {'ask_price': 8570000.0,
                            'ask_size': 0.8829,
                            'bid_price': 8549000.0,
                            'bid_size': 0.00067665},
                            {'ask_price': 8572000.0,
                            'ask_size': 0.34700000000000003,
                            'bid_price': 8548000.0,
                            'bid_size': 0.46794571},
                            {'ask_price': 8573000.0,
                            'ask_size': 0.30810000000000004,
                            'bid_price': 8547000.0,
                            'bid_size': 0.031170000000000003},
                            {'ask_price': 8575000.0,
                            'ask_size': 0.357,
                            'bid_price': 8546000.0,
                            'bid_size': 0.012871510000000001},
                            {'ask_price': 8576000.0,
                            'ask_size': 0.294,
                            'bid_price': 8545000.0,
                            'bid_size': 0.00617027},
                            {'ask_price': 8577000.0,
                            'ask_size': 0.434,
                            'bid_price': 8544000.0,
                            'bid_size': 0.00117041},
                            {'ask_price': 8579000.0,
                            'ask_size': 0.2931,
                            'bid_price': 8543000.0,
                            'bid_size': 0.04417054},
                            {'ask_price': 8581000.0,
                            'ask_size': 0.2967,
                            'bid_price': 8542000.0,
                            'bid_size': 0.0011706800000000001},
                            {'ask_price': 8585000.0,
                            'ask_size': 0.055,
                            'bid_price': 8541000.0,
                            'bid_size': 0.30117082},
                            {'ask_price': 8589000.0,
                            'ask_size': 1.1736,
                            'bid_price': 8540000.0,
                            'bid_size': 0.37128609},
                            {'ask_price': 8590000.0,
                            'ask_size': 0.050139699999999995,
                            'bid_price': 8539000.0,
                            'bid_size': 0.04417109}],
        'stream_type': 'REALTIME',
        'timestamp': 1577651862865,
        'total_ask_size': 7.37202867,
        'total_bid_size': 2.52538995,
        'type': 'orderbook'}
        """
        book = {}
        message = message['orderbook_units']
        book = {'name': self.name,
                'asks': {msg[AP]: msg[AS] for msg in message for v in msg.items()},
                'bids': {msg[BP]: msg[BS] for msg in message for v in msg.items()}}
        return book
from connector import Connector


class Bitfinex(Connector):
    
    def __init__(self, pairs, depth=None, **kwargs):
        super().__init__(pairs, depth, **kwargs)
        self.format_pairs = 't{}{}'.format(self.base.upper(), self.quote.upper())
        self.url = 'wss://api-pub.bitfinex.com/ws/2'
        self.payload = {"event": "subscribe",
                        "channel": "book",
                        "symbol": "tBTCUSD",
                        "prec": "P0",
                        "freq": "F0","len": 25}
        
    def on_data(self, data, data_type, flag=1):
        data = super().on_data(data, data_type, flag)
        self.zsock.send_json(data)
        self.zsock.recv()
        
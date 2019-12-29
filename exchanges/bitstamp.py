import time
from collections import OrderedDict as od

from connector import Connector
from defines import ASK, BID, BITSTAMP

class Bitstamp(Connector):
    
    id = BITSTAMP

    def __init__(self, pairs, depth=None, **kwargs):
        super().__init__(pairs, depth, **kwargs)
        self.l2_book = {}
        self.format_pairs = '{}{}'.format(self.base.lower(), self.quote.lower())
        self.url = 'wss://ws.bitstamp.net'
        self.payload = {"event": "bts:subscribe",
                        "data": {"channel": f"order_book_{self.format_pairs}"}}
        
    def on_data(self, data, data_type, flag):
        data = super().on_data(data, data_type, flag)
        self.zsock.send_json(self.book(data))
        self.zsock.recv()
    
    def book(self, message):
        """
        비트스탬프 기준 시간
        server_ts = float(f"{message['microtimestamp'][:10]}.{message['microtimestamp'][10:]}")
        
        웹소켓 콜백함수 기준 시간
        client_ts = timestamp
        """
        # 웹소켓 연결 성공 시
        if "bts:subscription_succeeded" in message:
            pass
        
        # # 비트스탬프는 모든 메시지를 message['data']로 접근
        message = message['data']
        
        self.l2_book = {'name': self.name,
                        ASK: od({x[0]: x[1] for x in message[ASK][:self.depth]}),
                        BID: od({x[0]: x[1] for x in message[BID][:self.depth]})}
        return self.l2_book
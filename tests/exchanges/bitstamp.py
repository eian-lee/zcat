from connector import Connector
from constants import BITSTAMP
from decimal import Decimal
import time

class Bitstamp(Connector):
    
    id = BITSTAMP

    def __init__(self, pairs, depth=None, **kwargs):
        super().__init__(pairs, depth, **kwargs)
        self.format_pairs = '{}{}'.format(self.base.lower(), self.quote.lower())
        self.url = 'wss://ws.bitstamp.net'
        self.payload = {'event': 'bts:subscribe',
                        'data': {'channel': 'order_book_%s' % self.format_pairs}}
        
    def on_data(self, data, data_type, flag):
        data, recv_at = super().on_data(data, data_type, flag)
        self.zsock.send_json(self.message_handler(data, recv_at))
        # self.zsock.send_json(data)
        self.zsock.recv()
    
    def message_handler(self, message, timestamp):
        # 웹소켓 연결 성공 시
        if "bts:subscription_succeeded" in message:
            pass
        
        # # 비트스탬프는 모든 메시지를 message['data']로 접근
        message = message['data']
        
        # # 비트스탬프 기준 시간
        # server_ts = float(f"{message['microtimestamp'][:10]}.{message['microtimestamp'][10:]}")
        server_ts = message['microtimestamp']
        
        # # 웹소켓 콜백함수 기준 시간
        client_ts = timestamp * 1000000
        
        
        return self.convert(
            name=self.name,
            bids=message['bids'][:self.depth],
            asks=message['asks'][:self.depth],
            server=server_ts,
            client=client_ts
        )
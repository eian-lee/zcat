
import gzip
from connector import Connector
from constants import HUOBI

# 후오비 글로벌: 'wss://api.huobi.pro/ws'
# 후오비 코리아: 'wss://api-cloud.huobi.co.kr/ws'

class Huobi(Connector):
    
    id = HUOBI
    
    def __init__(self, pairs, depth=None, **kwargs):
        super().__init__(pairs, depth, **kwargs)
        self.url = 'wss://api-cloud.huobi.co.kr/ws'
        self.format_pairs = '{}{}'.format(self.base.lower(), self.quote.lower())
        self.payload = {"sub": "market.%s.depth.step0" % self.format_pairs,
                        "id": "%s" % self.hash}
        
        
    def on_data(self, data, data_type, flag):
        data = super().on_data(data, data_type, flag)
        self.zsock.send_json(self.message_handler(data))
        self.zsock.recv()
        
    def message_handler(self, message):
        # 후오비 쓰지말 것, 실시간이 아님(1초 간격으로 보내줌)
        return self.convert(name=self.id,
                            symbol=self.pairs,
                            asks=message['tick']['asks'][:self.depth],
                            bids=message['tick']['bids'][:self.depth],
                            timestamp=self.nonce())
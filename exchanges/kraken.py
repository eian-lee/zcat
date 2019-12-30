
from itertools import islice
from connector import Connector
from defines import ASK, BID, PRICE, SIZE, KRAKEN
from tools.parallel import update_asks_bids

class Kraken(Connector):
    
    id = KRAKEN
    
    def __init__(self, pairs, depth, **kwargs):
        super().__init__(pairs, depth, **kwargs)
        self.format_pairs = "{}/{}".format(self.base.upper(), self.quote.upper())
        self.url = 'wss://ws.kraken.com'
        self.payload = {'event': 'subscribe',
                        'pair': ["%s" % self.format_pairs],
                        'subscription': {'name': 'book'}}
        
        # 오더북 설정
        self.orderbook = {}
        
    def on_data(self, data, data_type, flag):
        data = super().on_data(data, data_type, flag)
        self.zsock.send_pyobj(self.handler(data))
        self.zsock.recv_pyobj()
    
    def handler(self, message: list):
        message = message[1:-2]
        # 스냅샷 저장
        if 'as' in message[0]:
            self.orderbook = {'name': self.name,
                              'asks': {x[PRICE]: x[SIZE] for x in message[0]['as']},
                              'bids': {x[PRICE]: x[SIZE] for x in message[0]['bs']}}
            return self.orderbook
        
        """ 1. ASK 또는 BID 주문리스트 응답예제
        >>> [
             {"a": [["5541.30000","2.50700000","1534614248.456738","r"],
                    ["5542.50000", "0.40100000", "1534614248.456738"]]}, ...
            ]
        """
        for msg in message:
            for key, value in msg.items():
                # 주문타입 판단
                side = ASK if key == 'a' else BID
                # 현재 코드블럭에 진입하면
                # [price, size, timestamp, "r"] 로 포맷된 상태
                # 가변인자를 사용하여 price, size만 가져온다
                for price, size, *_ in value:
                    # 업데이트된 가격이 내 오더북에 있는 경우
                    if price in self.orderbook[side]:
                        # 수량이 0이 아닌 경우
                        if float(size) != 0:
                            # 내 오더북의 주문을 갱신
                            self.orderbook[side].update({price: size})
                        # 수량이 0인 경우 삭제
                        del self.orderbook[side][price]
                    # 업데이트된 가격이 내 오더북에 없는 경우
                    if float(size) != 0:
                        # 수량이 0이 아닌 경우에만 삽입
                        self.orderbook[side].update({price: size})
                        # 정렬 후 딕셔너리 슬라이싱으로 깊이 유지
                        self.orderbook[side] = dict(islice(sorted(self.orderbook[side].items()), self.depth))
                        
        """ 2. ASK & BID 동시에 수신시 응답예제
        >>> [
             {"a": [["5541.30000", "2.50700000", "1534614248.456738", "r"],
                    ["5542.50000", "0.40100000", "1534614248.456738"]]},
                    ... ],
             {"b": [["5531.30000", "2.50700000", "1534614248.456738", "r"],
                    ["5532.50000", "0.40100000", "1534614248.456738"]]},
                    ... ],
            ]
        """
        # 동시에 수신된 경우엔 message의 길이는 2로 고정
        if len(message) == 2:
            # ASK, BID 주문을 언패킹
            a, b = message
            # 크라켄은 수신된 리스트의 길이 제한이 없음
            # 위 응답예제를 길이와 상관 없이 동시에 (가격, 수량)으로 포맷; 함수주석 참고
            asks, bids = update_asks_bids(a, b)
            for index, orders in enumerate((asks, bids)):
                # 주문타입 판단
                side = ASK if index == 0 else BID
                for price, size in orders:
                    # 업데이트된 가격이 내 오더북에 있는지 멤버쉽 연산자로 체크
                    if price in self.orderbook[side]:
                        # 수량이 0이 아닌 경우
                        if float(size) != 0:
                            # 내 오더북의 가격을 갱신
                            self.orderbook[side].update({price: size})
                        # 수량이 0인 경우 삭제
                        del self.orderbook[side][price]
                    # 업데이트된 가격이 내 오더북에 없는 경우
                    if float(size) != 0:
                        # 수량이 0이 아닌 경우에만 삽입
                        self.orderbook[side].update({price: size})
                        # 정렬 후 오더북 깊이 유지
                        self.orderbook[side] = dict(islice(sorted(self.orderbook[side].items()), self.depth))
        return self.orderbook
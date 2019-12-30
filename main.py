
import sys
import time
from multiprocessing import Process
from pprint import pprint

import zmq
import ujson as json

from exchanges.bitstamp import Bitstamp
from exchanges.kraken import Kraken
from exchanges.bitfinex import Bitfinex
from exchanges.upbit import Upbit
from tools.parallel import calculate
from tools.threads import threads
from defines import ZMQ_PORT



def main():
    ctx = zmq.Context()
    socket = ctx.socket(zmq.REP)
    socket.bind("tcp://*:%s" % ZMQ_PORT)
    # 거래소 객체 생성
    # bitstamp = Bitstamp(pairs='BTC/USD', depth=10)
    kraken = Kraken(pairs='BTC/USD', depth=10)
    bitfinex = Bitfinex(pairs='BTC/USD')
    # upbit = Upbit(pairs='BTC/KRW')
    threads(kraken, bitfinex)
    # 오더북 담을곳
    order1 = {}
    order2 = {}
    
    while True:
        message = json.loads(socket.recv())
        
        # 거래소 이름 검사
        try:
            if 'Kraken' == message['name']:
                order1 = message
            if 'Bitfinex' == message['name']:
                order2 = message
        
            # order1과 order2에 값이 있을 때
            if (order1 and order2):
                pprint(order1)
                # case1, case2 = calculate(order1, order2)
                # 크라켄 ASK 가격 1,2,3 ... N / 비트파이넥스 BID 가격 1,2,3 ... N
                # 비트파이넥스 BID 가격 1.2.3 ... N / 크라켄 ASK 가격 1.2.3 ... N
                # 각 주문인덱스 끼리 교차계산, 인덱스 N이 5인경우 
                # BestOffer부터 5틱 즉, 10가지 계산을 순차가 아닌 동시성으로 처리
                # 이는 TCP 통신으로 누락이 있을 수 있어 BestOffer만 계산하면 위험하기때문
                # print(f"Case1: {case1[:3]}\nCase2: {case2[:3]}\n")
            socket.send_json(message)
        except TypeError:
            continue

            
if __name__ == "__main__":
    main()

import time
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


def main(port=5555):
    ctx = zmq.Context()
    socket = ctx.socket(zmq.REP)
    socket.bind("tcp://*:%s" % ZMQ_PORT)
    
    # 거래소 객체 생성
    # bitstamp = Bitstamp(pairs='BTC/USD', depth=10)
    kraken = Kraken(pairs='BTC/USD', depth=10)
    bitfinex = Bitfinex(pairs='BTC/USD')
    upbit = Upbit(pairs='BTC/KRW')
    
    # 스레드 생성
    threads(kraken, bitfinex, upbit)
    
    while True:
        message = socket.recv_pyobj()
        pprint(message)
        socket.send_json(message)
            
if __name__ == "__main__":
    main()
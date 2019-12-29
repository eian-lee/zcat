
import time
from pprint import pprint

import zmq
import ujson as json

from exchanges.bitstamp import Bitstamp
from exchanges.kraken import Kraken
from exchanges.bitfinex import Bitfinex

from tools.parallel import calculate
from core.starter import starter


def main(port=5590):
    ctx = zmq.Context()
    socket = ctx.socket(zmq.REP)
    socket.bind("tcp://*:%s" % port)
    
    # order1 = order2 = order3 = None
    
    # 거래소 객체 생성
    # bitstamp = Bitstamp(pairs='BTC/USD', depth=10)
    # kraken = Kraken(pairs='BTC/USD', depth=10)
    bitfinex = Bitfinex(pairs='BTC/USD')
    
    # 스레드 생성
    starter(bitfinex)
    while True:
        message = socket.recv_pyobj()
        print(message)
        socket.send_json(message)
            
if __name__ == "__main__":
    main()
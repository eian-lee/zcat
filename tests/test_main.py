import zmq
import time
import ujson as json
from pprint import pprint
from exchanges.bitstamp import Bitstamp
from exchanges.kraken import Kraken

from strategy.calc import calculate
from core.starter import starter

PORT = 5591


def main():
    ctx = zmq.Context()
    socket = ctx.socket(zmq.REP)
    socket.bind("tcp://*:%s" % PORT)
     
    order1 = None
    order2 = None
    
    bitstamp = Bitstamp(pairs='BTC/USD', depth=3)
    # kraken = Kraken(pairs='BTC/USD', depth=3)

    starter(bitstamp)
    
    while True:
        message = json.loads(socket.recv())
        print(message)
        # if message['name'] == 'Kraken':
            # order1 = message
        # elif message['name'] == 'Bitstamp':
            # order2 = message
    
        # if order1 and order2:
            # case1, case2 = calculate(order1, order2), calculate(order2, order1)
            # calculate(order1, order2)
            # print(order1)
            
        socket.send_json(message)
            
if __name__ == "__main__":
    main()
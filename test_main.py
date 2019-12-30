
import sys
import time
import multiprocessing
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


def server(port=ZMQ_PORT):
    ctx = zmq.Context()
    socket = ctx.socket(zmq.REP)
    socket.bind("tcp://*:%s" % port)
    
    while True:
        message = socket.recv_pyobj()
        
    
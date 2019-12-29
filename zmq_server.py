import zmq
import threading
import ujson as json

PORT = 5590

class ZMQServer:
    
    def __init__(self, ctx=None, addr=None):
        self.ctx = ctx or zmq.Context()
        self.addr = addr or "tcp://*:%s" % PORT
        self.zsock = self.ctx.socket(zmq.REP)
    
import zmq
import uuid

PORT = 5590

class ZMQClient:
    id = 'NotImplmented'
    
    def __init__(self, ctx=None, addr=None):
        self.hash = str(uuid.uuid4)
        self.uuid = self.id + self.hash
        self.ctx = ctx or zmq.Context()
        self.zsock = self.ctx.socket(zmq.REQ)
        self.addr = addr or "tcp://localhost:%s" % PORT

        
    


import uuid
import hashlib
import logging
import ujson as json
import websocket
import datetime
import zmq

LOG = logging.getLogger(__name__)

class Connector(object):
    
    id = "NotImplemented"
    
    def __init__(self, pairs, depth, ctx=None, addr=None, port=5555):
        self.pairs = pairs
        self.depth = depth
        self.base = self.pairs.split('/')[0]
        self.quote = self.pairs.split('/')[1]
        self.format_pairs = None
        self.url = None
        self.payload = None
        self.name = self.__class__.__name__
        
        # Payload에 고유값이 필요한 거래소설정
        self.hash = str(uuid.uuid4)
        self.uuid = self.id + self.hash
        
        # Websocket, ZMQ Socket 객체생성
        self.ws = None
        self.ctx = ctx or zmq.Context()
        self.addr = addr or "tcp://localhost:%s" % port
        self.zsock = self.ctx.socket(zmq.REQ)
        self.zsock.connect(self.addr)

    def nonce(self):
        return datetime.datetime.now().strftime("%Y-%m-%d  %H:%M:%fS")
    
    def on_open(self):
        if self.ws.sock.connected:
            self.ws.send(json.dumps(self.payload))
    
    def on_data(self, data, data_type: str, flag=1):
        return json.loads(data)
    
    def on_error(self, error):
        """[1900-01-01  00:00:0000] ExchangeName Error...
        """
        LOG.debug(f"[{self.nonce()}] {self.name} {error}")
    
    def on_close(self):
        LOG.info(f"[{self.nonce()}] Websocket Connection has been closed")

    def connect(self):
        self.ws = websocket.WebSocketApp(
            self.url,
            on_open=self.on_open,
            on_data=self.on_data,
            on_error=self.on_error,
            on_close=self.on_close
        )
        self.ws.run_forever()
        
    def run(self):
        self.connect()

import logging
import ujson as json
import websocket
import datetime
from zmq_client import ZMQClient

Log = logging.getLogger(__name__)

class Connector(ZMQClient):
    
    def __init__(self, pairs, depth, **kwargs):
        super().__init__()
        self.pairs = pairs
        self.depth = depth
        self.base = self.pairs.split('/')[0]
        self.quote = self.pairs.split('/')[1]
        self.format_pairs = None
        self.url = None
        self.payload = None
        self.name = self.__class__.__name__
        
        # Websocket, ZMQ Socket 설정
        self.ws = None
        self.is_connected = False
        self.is_opened = False
        self.zsock.connect(self.addr)

    def nonce(self):
        return datetime.datetime.now().strftime('%H:%M:%S%f')

    def connect(self):
        self.ws = websocket.WebSocketApp(self.url,
                                         on_open=self.on_open,
                                         on_data=self.on_data,
                                         on_error=self.on_error,
                                         on_close=self.on_close)
        self.ws.run_forever()
        
    def run(self):
        self.connect()
        
    def on_open(self):
        self.is_connected = True
        if self.ws.sock.connected:
            self.ws.send(json.dumps(self.payload))
    
    def on_data(self, data, data_type: str, flag=1):
        return json.loads(data)
    
    def on_error(self, error):
        Log.debug(f'{self.id}: {error}')
        self.is_connected = False
        if self.ws.sock:
            self.ws.close()
            self.zsock.close()
    
    def on_close(self):
        Log.info('Websocket has closed')
        if self.is_connected:
            self.is_connected = False
            if self.ws.sock:
                self.ws.close()
                self.zsock.close()
    
    
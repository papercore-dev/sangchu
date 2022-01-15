import websocket, time, json, logging
from typing import TypeVar, Any
from _thread import start_new_thread

GatewayResponse = TypeVar("GatewayResponse")
GatewayRequest = TypeVar("GatewayRequest")

class GatewayBot:
    def __init__(self, token: Any):
        if not isinstance(token, str):
            raise TypeError
        
        self.ready = False
        self.token = token
        self.ws = websocket.WebSocket()

    def _send(self, request: GatewayRequest) -> GatewayResponse:
        logging.info(f"{request}를 디스코드 게이트웨이에 보내다!")
        self.ws.send(json.dumps(request))

    def _wait(self, ms: Any) -> GatewayResponse:
        time.sleep(ms / 1000)

    def _receive(self) -> GatewayResponse:
        response = self.ws.recv()
        if response:
            return json.loads(response)

    def _heartbeat(self, interval: Any) -> GatewayResponse:
        while True:
            self._wait(interval)
            _content = {
                "op": 1,
                "d": None
            }
            self._send(_content)

    def _login(self) -> GatewayResponse:
        self.ws.connect("wss://gateway.discord.gg/?v=6&encoding=json")
        _event = self._receive()
        _heartbeat_interval = _event["d"]["heartbeat_interval"]

        start_new_thread(self._heartbeat, (_heartbeat_interval, ))

        _payload = {
            "op": 2,
            "d": {
                "token": self.token,
                "properties": {
                    "$os": "iOS",
                    "$browser": "Discord Android",
                    "$device": "phone"
                }
            }
        }
        self._send(_payload)
        self.ready = True

        if self.ready:
            print("봇이 준비되다?!??!?!?!?!?")

        while True:
            _event = self._receive()
            op = _event["op"]

            if op >= 11:
                logging.info("심장 박동을 보내다!")

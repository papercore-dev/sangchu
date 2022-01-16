from time import sleep
from typing import Any
from extensions import run_on_low_level 

import websocket, ujson, logging

class Client:
    def __init__(self):
        self.ready = False
        self.token = None
        self.event = None
        self.ws = websocket.WebSocket()

    def send(self, request: Any) -> None:
        logging.info(f"{request}를 디스코드 게이트웨이에 보내다!")
        self.ws.send(ujson.dumps(request))

    def wait(self, ms: Any) -> Any:
        sleep(ms / 1000)

    def receive(self) -> dict:
        response = self.ws.recv()
        if response:
            return ujson.loads(response)

    def close(self) -> None:
        self.ws.close()

    @run_on_low_level
    def heartbeat(self, interval: Any) -> None:
        while True:
            self.wait(interval)
            content = {
                "op": 1,
                "d": None
            }
            self.send(content)

    def login(self, token: str) -> Any:
        self.token = token
        self.ws.connect("wss://gateway.discord.gg/?v=6&encoding=json")
        self.event = self.receive()
        heartbeat_interval = self.event["d"]["heartbeat_interval"]

        self.heartbeat(heartbeat_interval)

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
        self.send(_payload)
        self.ready = True

        if self.ready:
            logging.info("봇이 준비되다?!!??!")

        while True:
            self.event = self.receive()
            op = self.event["op"]

            if op >= 11:
                logging.info("심장 박동을 보내다!")

from time import sleep
from extensions import run_on_low_level
from tqdm import tqdm

import websocket, ujson

class Client:
    def __init__(self):
        self.ready = False
        self.token = None
        self.event = None
        self.message = None
        self.ws = websocket.WebSocket()

    def send(self, request) -> None:
        print("게이트웨이에 요청을 보냄")
        self.ws.send(ujson.dumps(request))

    def wait(self, ms) -> None:
        sleep(ms / 1000)

    def receive(self) -> dict:
        response = self.ws.recv()
        if response:
            return ujson.loads(response)

    def close(self) -> None:
        self.ws.close()

    @run_on_low_level
    def heartbeat(self, interval: float) -> None:
        while True:
            self.wait(interval)
            content = {
                "op": 1,
                "d": None
            }
            self.send(content)

    def login(self, token: str) -> None:
        print("봇 준비")
        for _ in tqdm(range(1)):
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
            print("봇이 준비됨")

        while True:
            self.event = self.receive()
            op = self.event["op"]

            if op >= 11:
                print("심장박동 보냄")

import json, websockets, asyncio

from channels.exceptions import DenyConnection
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer

from .models import Task
from .process import CTFProcess


class TerminalConsumer(WebsocketConsumer):

    def start_process(self, program) -> CTFProcess:
        task = Task.objects.get(id=self.task_id)
        module = task.module.name

        return CTFProcess(f"{module}/{program}", task.secret)

    def connect(self):
        program = self.scope["url_route"]["kwargs"]["program"]
        self.task_id = self.scope["url_route"]["kwargs"]["task_id"]

        self.process = self.start_process(program)
        return super().connect()

    def disconnect(self, code):
        return super().disconnect(code)

    def receive(self, text_data=None, bytes_data=None):
        json_data = json.loads(text_data)
        command = json_data["command"]

        if command == "handshake":
            output = self.process.readline()

            if output is not None:
                self.send_bytes(output)

        elif command == "input":
            input = json_data["value"]

            self.process.writeline(input)
            output = self.process.readline()

            if output is not None:
                self.send_bytes(output)

        return super().receive(text_data, bytes_data)

    def send_bytes(self, bytes: bytes):
        decoded = bytes.decode()
        self.send(decoded)


class ProxyConsumer(AsyncWebsocketConsumer):
    """
    Django Channels websockets consumer that forwards websocket connections to a Docker container.
    Based on https://gist.github.com/brianglass/e3184341afe63ed348144753ee62dce5
    """

    def __init__(self, endpoint: str, *args: object, **kwargs: object) -> None:
        """Create a new proxy consumer for a websocket server at the specified endpoint"""
        super().__init__(*args, **kwargs)
        self.endpoint = endpoint
        self.upstream_socket = None
        self.forward_upstream_task = None

    async def connect(self) -> None:
        # Attempt to connect to the endpoint to proxy
        try:
            self.upstream_socket = await websockets.connect(self.endpoint)
        except websockets.InvalidURI:
            print("The container endpoint was not reachable.")
            raise DenyConnection()

        # Accept the incoming connection with the same subprotocol.
        await self.accept(self.upstream_socket.subprotocol)

        self.forward_upstream_task = asyncio.create_task(self.forward_upstream())

    async def forward_upstream(self):
        try:
            async for data in self.upstream_socket:
                if hasattr(data, "decode"):
                    await self.send(bytes_data=data)
                else:
                    await self.send(text_data=data)
        except asyncio.exceptions.CancelledError:
            # This is triggered by the consumer itself when the client connection is terminating.
            await self.upstream_socket.close()
        except websockets.ConnectionClosedError:
            # The target probably closed the connection.
            await self.close()

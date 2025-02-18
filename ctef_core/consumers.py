import json
from channels.generic.websocket import WebsocketConsumer

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

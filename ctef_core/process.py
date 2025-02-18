import os
from subprocess import Popen, PIPE


class CTFProcess:
    """
    Temporary implementation of process management to communicate over stdin/stdout.
    See https://eli.thegreenplace.net/2017/interacting-with-a-long-running-child-process-in-python/ for motivation.
    """

    def __init__(self, executable, secret) -> None:
        """Starts a new process with communciation over stdin/stdout. Injects task secret into the program environment."""
        env = os.environ
        env["CTF_SECRET"] = secret

        self.process = Popen(executable, env=env, stdin=PIPE, stdout=PIPE, stderr=PIPE)

    def __del__(self):
        # Close the process stdin and terminate when object destroyed.
        self.process.stdin.close()
        self.process.terminate()

    def readline(self) -> bytes | None:
        """Reads on line from the standard output of the running process."""

        if self.process.poll() is not None:
            return None

        return self.process.stdout.readline()

    def writeline(self, line: str):
        """Write a line to the standard input of the running process."""

        if self.process.poll() is None:
            self.process.stdin.write(f"{line}\n".encode())
            self.process.stdin.flush()

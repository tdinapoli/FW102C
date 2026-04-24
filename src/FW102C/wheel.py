from .pyserial_client import SerialClient
from . import commands


class Wheel:
    MAX_POS: int = 12
    MIN_POS: int = 1

    def __init__(
        self,
        port: str,
        baudrate: int = 115200,
        timeout: float = 1.0,
        line_ending: str = "\r",
    ):
        self._serial = SerialClient(
            port, baudrate=baudrate, timeout=timeout, line_ending=line_ending
        )

    def goto_pos(self, pos: int):
        assert self.MIN_POS <= pos <= self.MAX_POS
        self._serial.write_command(commands.build_command(commands.POS, params=[pos]))

    def get_pos(self):
        return int(
            self._serial.query_command(
                commands.build_command(commands.POS, query=True)
            ).split("\n")[1]
        )

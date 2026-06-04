import logging
from typing import Literal

from .pyserial_client import SerialClient
from . import commands

logger = logging.getLogger(__name__)


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

    def goto_pos(self, pos: Literal[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]):
        assert self.MIN_POS <= pos <= self.MAX_POS, (
            f"Invalid position {pos} for wheel with min {self.MIN_POS} and max {self.MAX_POS}"
        )
        logger.info(f"Filter wheel going to position {pos}")
        self._serial.write_command(commands.build_command(commands.POS, params=[pos]))

    def get_pos(self):
        logger.info("Retrieving filter wheel position")
        return int(
            self._serial.query_command(
                commands.build_command(commands.POS, query=True)
            ).split("\n")[1]
        )

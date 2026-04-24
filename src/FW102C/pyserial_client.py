"""
Minimal pyserial helper that mirrors the SCPI-style command construction used by the
Jeti board driver and routes traffic over a serial port.
"""

import logging
from enum import Enum
from typing import Iterable, Optional
import re

import serial


LOGGER = logging.getLogger(__name__)


def parse_float_value(msg: str):
    try:
        result = re.findall(r"[0-9]+\.?[0-9]*|[0-9]*\.?[0-9]+", msg)
        if len(result) == 0:
            raise ValueError(
                f"Expected to find a floating point number, instead found '{msg}'"
            )
        return result[0]
    except Exception as e:
        raise ValueError(
            f"Parsing message '{msg}' for a floating point number raise exception {e}"
        )


class SerialClient:
    """Wraps pyserial to send commands and convert responses to Python types."""

    def __init__(
        self,
        port: str,
        baudrate: int = 115200,
        timeout: float = 1.0,
        line_ending: str = "\r",
    ):
        self._serial = serial.Serial(port=port, baudrate=baudrate, timeout=timeout)
        self._line_ending = line_ending.encode("ascii")

    def __enter__(self):
        return self

    def __exit__(self):
        self._serial.close()

    def set_timeout(self, timeout: float) -> None:
        self._serial.timeout = timeout

    def write_command(self, command: str) -> None:
        LOGGER.debug("Sending: %s", command)
        self._serial.write(command.encode("ascii") + self._line_ending)
        self._serial.flush()

    def query_command(self, command: str) -> str:
        LOGGER.debug(f"Sending {command}")
        self.write_command(command)
        current_text = self.read_text_line()
        text = ""
        while current_text != "":
            text += current_text.replace("\r", "\n")
            current_text = self.read_text_line()
        return text

    def read_text_line(self) -> str:
        raw = self._serial.readline()
        text = raw.decode(errors="ignore").strip()
        LOGGER.debug("Received text: %s", text)
        return text

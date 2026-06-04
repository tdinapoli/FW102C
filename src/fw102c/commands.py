from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Optional


class _StrEnum(str, Enum):
    @staticmethod
    def _generate_next_value_(name, start, count, last_values) -> str:  # type: ignore[override]
        return name.lower()


class Commands(_StrEnum):
    POS = "pos"
    PCOUNT = "pcount"
    TRIG = "trig"
    SPEED = "speed"
    SENSORS = "sensors"
    SAVE = "save"
    IDN = "idn"


@dataclass
class Command:
    text: str
    writable: bool
    param_types: list[type] = field(default_factory=list)
    subcommands: list[Command] = field(default_factory=list)


def build_command(
    *commands: Command,
    query: bool = False,
    params: list | None = None,
    command_sep: str = ":",
    param_sep: str = ",",
    command_param_sep: str = "=",
) -> str:
    if params and not commands[-1].writable:
        raise ValueError("Cannot give params for a not writable command")
    if not params:
        params = []
        command_param_sep = ""
    for param, param_type in zip(params, commands[-1].param_types):
        assert type(param) is param_type
    params = [str(param) for param in params]
    questionmark = "?" if query else ""
    return (
        command_sep.join([command.text for command in commands])
        + command_param_sep
        + param_sep.join(params)
        + questionmark
    )


POS = Command(text="pos", writable=True, param_types=[int], subcommands=[])
PCOUNT = Command(text="pcount", writable=True, param_types=[int], subcommands=[])
TRIG = Command(text="trig", writable=True, param_types=[int], subcommands=[])
SPEED = Command(text="speed", writable=True, param_types=[int], subcommands=[])
SENSORS = Command(text="sensors", writable=True, param_types=[int], subcommands=[])
SAVE = Command(text="save", writable=False, param_types=[], subcommands=[])
IDN = Command(text="idn", writable=False, param_types=[], subcommands=[])

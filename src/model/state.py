"""
Represents the state of the looper.
"""

from enum import Enum

from config.audio_config import MAX_CHUNKS_PER_TRACK


class Status(Enum):
    """
    Represents the state of the looper.
    """
    EMPTY = 0
    RECORDING_FIRST_TRACK = 1
    PLAYING = 2
    RECORDING_SUBSEQUENT_TRACK = 3


class State:
    """
    Contains the variables that make up the state of the looper.
    """
    status = Status.EMPTY
    current_chunk = 0
    last_chunk = MAX_CHUNKS_PER_TRACK - 1

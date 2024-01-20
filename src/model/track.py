"""Contains the Track class"""

import numpy as np

from config.audio_config import CHUNK_SIZE, MAX_CHUNKS_PER_TRACK


class Track:
    """This represents a single audio recording."""

    audio = np.zeros([MAX_CHUNKS_PER_TRACK, CHUNK_SIZE], dtype=np.int16)

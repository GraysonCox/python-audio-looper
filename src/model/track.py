import numpy as np

from config.audio_config import CHUNK_SIZE, MAX_CHUNKS_PER_TRACK, CHUNK_SIZE


class Track:
    audio = np.zeros([CHUNK_SIZE * MAX_CHUNKS_PER_TRACK, CHUNK_SIZE], dtype=np.int16)

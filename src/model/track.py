import numpy as np

from config.audio_config import CHUNK_SIZE, MAX_CHUNKS_PER_TRACK, CHUNK_SIZE


class Track:
    audio = np.zeros([MAX_CHUNKS_PER_TRACK, CHUNK_SIZE], dtype=np.int16)




"""
CHUNK_SIZE = 5
[]

"""
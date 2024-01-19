import pyaudio
import numpy as np
import multiprocessing
from enum import Enum

SAMPLE_RATE = 44100
CHUNK_SIZE = 1024
MAX_CHUNKS_PER_TRACK = 10000
MAX_TRACKS = 10


class State(Enum):
    EMPTY = 0
    RECORDING_FIRST_TRACK = 1
    PLAYING = 2
    RECORDING_SUBSEQUENT_TRACK = 3


class Track:
    audio = np.zeros([CHUNK_SIZE * MAX_CHUNKS_PER_TRACK, CHUNK_SIZE], dtype=np.int16)


class Looper:
    def __init__(self):
        self.state = State.EMPTY
        self.current_chunk = 0
        self.last_chunk = MAX_CHUNKS_PER_TRACK - 1

        self.pa = pyaudio.PyAudio()
        self.tracks = [Track() for _ in range(0, MAX_TRACKS)]
        self.looping_stream = self.pa.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=SAMPLE_RATE,
            input=True,
            output=True,
            input_device_index=0,
            output_device_index=1,
            frames_per_buffer=CHUNK_SIZE,
            start=True,
            stream_callback=lambda in_data, _1, _2, _3: self._looping_callback(in_data),
        )

    def toggle_recording(self):
        if self.state == State.EMPTY:
            self.state = State.RECORDING_FIRST_TRACK
        elif self.state == State.RECORDING_FIRST_TRACK:
            self.state = State.PLAYING
            self.last_chunk = self.current_chunk
            self.current_chunk = 0
        elif self.state == State.PLAYING:
            self.state = State.RECORDING_FIRST_TRACK  # TODO: Add new state.

    def clear(self):
        self.state = State.EMPTY
        self.current_chunk = 0
        self.last_chunk = MAX_CHUNKS_PER_TRACK - 1

        self.tracks = [Track() for i in range(0, MAX_TRACKS)]

    def close(self):
        self.looping_stream.close()
        self.pa.terminate()

    def _looping_callback(self, in_data):
        # Do nothing if EMPTY.
        if self.state == State.EMPTY:
            return (np.zeros([CHUNK_SIZE], dtype=np.int16), pyaudio.paContinue)

        # Do recording if desired.
        if self.state in [
            State.RECORDING_FIRST_TRACK,
            State.RECORDING_SUBSEQUENT_TRACK,
        ]:
            self.tracks[0].audio[self.current_chunk, :] = np.copy(
                np.frombuffer(in_data, dtype=np.int16)
            )

        # Get desired audio for output.
        if self.state in [State.PLAYING, State.RECORDING_SUBSEQUENT_TRACK]:
            output_chunk = self.tracks[0].audio[
                self.current_chunk : self.current_chunk + CHUNK_SIZE
            ]
        else:
            output_chunk = np.zeros([CHUNK_SIZE], dtype=np.int16)

        # Increment counter.
        self.current_chunk = (self.current_chunk + 1) % self.last_chunk
        return (output_chunk, pyaudio.paContinue)

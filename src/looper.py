import pyaudio
import numpy as np
import multiprocessing
from enum import Enum

SAMPLE_RATE = 44100
CHUNK_SIZE = 1024
MAX_CHUNKS_PER_TRACK = 10000


class State(Enum):
    EMPTY = 0
    RECORDING = 1
    PLAYING = 2


class Looper:
    def __init__(self):
        self.pa = pyaudio.PyAudio()
        self.state = State.EMPTY
        self.recording = np.zeros([CHUNK_SIZE * MAX_CHUNKS_PER_TRACK, CHUNK_SIZE], dtype=np.int16)
        self.current_chunk = 0
        self.last_chunk = MAX_CHUNKS_PER_TRACK

        def _looping_callback(in_data, _frame_count, _time_info, _status):
            if self.state == State.EMPTY:
                return (np.zeros([CHUNK_SIZE], dtype=np.int16), pyaudio.paContinue)

            if self.state == State.RECORDING:
                current_rec_buffer = np.copy(np.frombuffer(in_data, dtype=np.int16))
                self.recording[self.current_chunk, :] = current_rec_buffer
                output_chunk = np.zeros([CHUNK_SIZE], dtype=np.int16)
            elif self.state == State.PLAYING:
                output_chunk = self.recording[self.current_chunk : self.current_chunk + CHUNK_SIZE]

            self.current_chunk = (self.current_chunk + 1) % self.last_chunk
            return (output_chunk, pyaudio.paContinue)

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
            stream_callback=_looping_callback,
        )

    def toggle_recording(self):
        if self.state == State.EMPTY:
            self.state = State.RECORDING
        elif self.state == State.RECORDING:
            self.state = State.PLAYING
            self.last_chunk = self.current_chunk
            self.current_chunk = 0
        elif self.state == State.PLAYING:
            self.state = State.RECORDING

    def clear(self):
        self.looping_stream.close()
        self.pa.terminate()
        self.state = State.EMPTY
        self.recording = np.zeros([CHUNK_SIZE], dtype=np.int16)
        self.current_chunk = 0
        self.last_chunk = MAX_CHUNKS_PER_TRACK

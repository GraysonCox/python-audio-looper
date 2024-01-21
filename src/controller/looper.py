import pyaudio
import numpy as np

from config.audio_config import (
    MAX_CHUNKS_PER_TRACK,
    MAX_TRACKS,
    SAMPLE_RATE,
    CHUNK_SIZE,
)
from model.state import Status, State
from model.track import Track


class Looper:
    def __init__(self, state, tracks):
        self.state = state
        self.tracks = tracks

        self.pa = pyaudio.PyAudio()
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
            stream_callback=lambda in_data, frame_count, _2, _3: self._looping_callback(
                in_data, frame_count
            ),
        )

    def toggle_recording(self):
        """
        Control state of looper.
        """
        if self.state.status == Status.EMPTY:
            self.state.status = Status.RECORDING_FIRST_TRACK
        elif self.state.status == Status.RECORDING_FIRST_TRACK:
            self.state.status = Status.PLAYING
            self.state.last_chunk = self.state.current_chunk
            self.state.current_chunk = 0
            self.state.num_tracks_used = 1
        elif self.state.status == Status.PLAYING:
            self.state.status = Status.RECORDING_SUBSEQUENT_TRACK
        elif self.state.status == Status.RECORDING_SUBSEQUENT_TRACK:
            self.state.status = Status.PLAYING
            self.state.num_tracks_used += 1

    def clear(self):
        """
        Reset looper to initial state.
        """
        self.state.status = Status.EMPTY
        self.state.current_chunk = 0
        self.state.last_chunk = MAX_CHUNKS_PER_TRACK - 1

        self.tracks = [Track() for i in range(0, MAX_TRACKS)]  # TODO: This won't work.

    def close(self):
        """
        Close everything.
        """
        self.looping_stream.close()
        self.pa.terminate()

    def _looping_callback(self, in_data, frame_count):
        # Do nothing if EMPTY.
        if self.state.status == Status.EMPTY:
            return (np.zeros([frame_count], dtype=np.int16), pyaudio.paContinue)

        # Do recording if desired.
        if self.state.status in [
            Status.RECORDING_FIRST_TRACK,
            Status.RECORDING_SUBSEQUENT_TRACK,
        ]:
            recorded_chunk = np.copy(np.frombuffer(in_data, dtype=np.int16))
            self.tracks[self.state.num_tracks_used].audio[self.state.current_chunk] = recorded_chunk

        # Get desired audio for output.
        if self.state.status in [Status.PLAYING, Status.RECORDING_SUBSEQUENT_TRACK]:
            output_chunk = np.copy(self.tracks[0].audio[self.state.current_chunk])
            for track in range(1, self.state.num_tracks_used):
                for i in range(0, frame_count):
                    output_chunk[i] += self.tracks[track].audio[self.state.current_chunk][i]
        else:
            output_chunk = np.zeros([frame_count], dtype=np.int16)

        # Increment counter.
        self.state.current_chunk = (
            self.state.current_chunk + 1
        ) % self.state.last_chunk

        return (output_chunk, pyaudio.paContinue)

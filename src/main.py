"""
The main file.
"""

from config.audio_config import MAX_TRACKS
from controller.looper import Looper
from model.state import State
from model.track import Track


if __name__ == "__main__":
    state = State()
    tracks = [Track() for _ in range(0, MAX_TRACKS)]
    the_looper = Looper(state, tracks)

    input("Press ENTER to start recording.")
    the_looper.toggle_recording()
    input("Press ENTER to start looping.")
    the_looper.toggle_recording()
    input("Press ENTER to quit.")
    the_looper.close()

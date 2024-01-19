import looper

if __name__ == "__main__":
    the_looper = looper.Looper()
    input("Press ENTER to start recording.")
    the_looper.toggle_recording()
    input("Press ENTER to start looping.")
    the_looper.toggle_recording()
    input("Press ENTER to quit.")
    the_looper.close()

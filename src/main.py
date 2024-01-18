import looper

if __name__ == "__main__":

    my_looper = looper.Looper()
    input("Press ENTER to start recording.")
    my_looper.toggle_recording()
    input("Press ENTER to start looping.")
    my_looper.toggle_recording()
    input("Press ENTER to quit.")
    my_looper.clear()

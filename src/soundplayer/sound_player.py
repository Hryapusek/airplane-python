# Import the necessary modules
from states import *  # Import all states from the states module
from threading import Thread, Event  # Import Thread and Event from the threading module
from pygame import mixer  # Import mixer from the pygame module
from asyncio import sleep, run  # Import sleep and run from the asyncio module

# Initialize the mixer and load the beep sound
mixer.init()
mixer.music.load('beep.mp3')

class SoundPlayer:
    def __init__(self) -> None:
        # Initialize the thread, stop flag, and state
        self.__thread: Thread = None
        self.__stop_flag = Event()
        self.__state: State = None

    def set_state(self, new_state: State):
        # Check if the new state is the same as the current state
        if self.__state == new_state:
            return
        # If a thread is running, stop it and wait for it to finish
        if self.__thread is not None and self.__thread.is_alive():
            self.__stop_flag.set()
            self.__thread.join()
        # Clear the stop flag
        self.__stop_flag.clear()
        # Set the new state and start the corresponding thread
        if new_state == State.SAFE_DISTANCE:
            return
        elif new_state == State.DISTANCE_3:
            self.__thread = Thread(target=self.__play_sound, args=(900,), daemon=True)
        elif new_state == State.DISTANCE_2:
            self.__thread = Thread(target=self.__play_sound, args=(600,), daemon=True)
        elif new_state == State.DISTANCE_1:
            self.__thread = Thread(target=self.__play_sound, args=(300,), daemon=True)
        # Start the thread
        self.__thread.start()

    def __play_sound(self, interval_msec: int):
        # Play the sound in a loop until the stop flag is set
        while not self.__stop_flag.is_set():
            try: 
                # Play the sound
                mixer.music.play()
            except:
                # Raise any exceptions that occur
                raise
            # Check if the stop flag is set
            if self.__stop_flag.is_set(): 
                return
            # Wait for the specified interval
            run(sleep(interval_msec/1000))

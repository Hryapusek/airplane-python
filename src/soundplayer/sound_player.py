from states import *
from threading import Thread, Event
from playsound import playsound
from asyncio import sleep, run

class SoundPlayer:
    def __init__(self) -> None:
        self.__thread: Thread = None
        self.__stop_flag = Event()
        self.__state: State = None

    def set_state(self, new_state: State):
        if self.__state == new_state:
            return
        if self.__thread is not None and self.__thread.is_alive():
            self.__stop_flag.set()
            self.__thread.join()
        self.__stop_flag.clear()
        if new_state == State.SAFE_DISTANCE:
            return
        elif new_state == State.DISTANCE_3:
            self.__thread = Thread(target=self.__play_sound, args=(900,), daemon=True)
        elif new_state == State.DISTANCE_2:
            self.__thread = Thread(target=self.__play_sound, args=(600,), daemon=True)
        elif new_state == State.DISTANCE_1:
            self.__thread = Thread(target=self.__play_sound, args=(300,), daemon=True)
        self.__thread.start()

    def __play_sound(self, interval_msec: int):
        while not self.__stop_flag.is_set():
            try:
                playsound("res/beep.mp3", block=False)
            except:
                pass
            if self.__stop_flag.is_set(): return
            run(sleep(interval_msec/1000))

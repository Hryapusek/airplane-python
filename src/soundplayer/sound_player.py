# Импортируем необходимые модули
from states import *  # Импортируем все состояния из модуля states
from threading import Thread, Event  # Импортируем Thread и Event из модуля threading
from pygame import mixer  # Импортируем mixer из модуля pygame
from asyncio import sleep, run  # Импортируем sleep и run из модуля asyncio

# Инициализируем микшер и загружаем звук beep
mixer.init()
mixer.music.load('beep.mp3')

class SoundPlayer:
    def __init__(self) -> None:
        # Инициализируем поток, флаг остановки и состояние
        self.__thread: Thread = None
        self.__stop_flag = Event()
        self.__state: State = None

    def set_state(self, new_state: State):
        # Проверяем, является ли новое состояние другим от текущего состояния
        if self.__state == new_state:
            return
        # Если поток работает, останавливаем его и ждем, пока он не завершится
        if self.__thread is not None and self.__thread.is_alive():
            self.__stop_flag.set()
            self.__thread.join()
        # Очищаем флаг остановки
        self.__stop_flag.clear()
        # Устанавливаем новое состояние и запускаем соответствующий поток
        if new_state == State.SAFE_DISTANCE:
            return
        elif new_state == State.DISTANCE_3:
            self.__thread = Thread(target=self.__play_sound, args=(900,), daemon=True)
        elif new_state == State.DISTANCE_2:
            self.__thread = Thread(target=self.__play_sound, args=(600,), daemon=True)
        elif new_state == State.DISTANCE_1:
            self.__thread = Thread(target=self.__play_sound, args=(300,), daemon=True)
        # Запускаем поток
        self.__thread.start()

    def __play_sound(self, interval_msec: int):
        # Проигрываем звук в цикле, пока не будет установлен флаг остановки
        while not self.__stop_flag.is_set():
            try: 
                # Проигрываем звук
                mixer.music.play()
            except:
                # Генерируем любые исключения, которые возникнут
                raise
            # Проверяем, установлен ли флаг остановки
            if self.__stop_flag.is_set(): 
                return
            # Ждем указанный интервал
            run(sleep(interval_msec/1000))

import datetime
import threading
from threading import Thread, Event
import time
import itertools
from string import ascii_letters
from queue import Queue
from pynput import keyboard

# def on_press(key):
#     print('Key %s pressed' % key)
#
# def on_release(key):
#     print('Key %s released' %key)
#
# listener = keyboard.Listener(
#     on_press=on_press,
#     on_release=on_release)
# listener.start()

MIN_LEN = 5
MAX_LEN = 26
QUANTUM = 450000  # nanosecond
TICK = QUANTUM * 8000
WORDS = ("BEttA", "glADE", "BrUTE")

ready_queue = Queue(maxsize=3)
wait_queue = Queue(maxsize=3)
block_event = Event()


def on_activate():
    print('Global hotkey activated!')


def for_canonical(f):
    return lambda k: f(listener.canonical(k))


class BruteThread(Thread):
    def __init__(self, name, word):
        Thread.__init__(self)
        self.name = name
        self.word = word
        self.__is_ready = False
        self.__count = 0
        self.__pause_event = Event()
        # self.__pause_event.set()

    def _simple_brute(self):
        for repeat in range(MIN_LEN, MAX_LEN):
            for i in itertools.product(ascii_letters, repeat=repeat):
                self.__count += 1
                # print(''.join(i))
                self.__pause_event.wait()
                if ''.join(i) == self.word:
                    return True
        return None

    def run(self):
        print(f"Thread '{self.name}' was born!")
        self.__is_ready = True
        if self._simple_brute() is not None:
            print(f"Thread '{self.name}' successfully completed! Word: {self.word} Combinations: {self.__count}")
        else:
            print(f"Thread '{self.name}' unsuccessfully finished! Word: {self.word} Combinations: {self.__count}")

    def pause(self):
        if self.__pause_event.is_set():
            print(f"Thread '{self.name}' paused")
            self.__pause_event.clear()

    def resume(self):
        if not self.__pause_event.is_set():
            print(f"Thread '{self.name}' resumed")
            self.__pause_event.set()

    def is_ready(self):
        return self.__is_ready

    def unready(self):
        self.__is_ready = not self.__is_ready


class Helper:
    def __init__(self):
        self.__active_thread = None

    def set_active_thread(self, thread):
        self.active_thread = thread

    def get_active_thread(self):
        return self.active_thread


threads = [BruteThread("Foo()", WORDS[0]), BruteThread("Bar()", WORDS[1]), BruteThread("Baz()", WORDS[2])]


def wait_for_tick_expire(thread):
    start = time.time_ns()
    while time.time_ns() - start < TICK and thread.is_ready():
        pass
    return


# Отправление/возвращение потока в/из нижней очереди


Lllecmepka = Helper()



def on_space():
    if wait_queue.qsize() >= 1:
        thread = wait_queue.get()
        thread.unready()
        print("Ожидание: ", [i.name for i in wait_queue.queue])
        print("---------->")
        ready_queue.put(thread)
        print("Готовность: ", [i.name for i in ready_queue.queue])
    else:
        if Lllecmepka.get_active_thread() is not None:
            thread = Lllecmepka.get_active_thread()
            thread.pause()
            thread.unready()
            wait_queue.put(thread)
            print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
            print("Готовность: ", [i.name for i in ready_queue.queue])
            print("Ожидание: ", [i.name for i in wait_queue.queue])
            print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
    return


hotkey = keyboard.HotKey(
    keyboard.HotKey.parse('<ctrl>+<alt>+k'),
    on_activate=on_space)

listener = keyboard.Listener(
    on_press=for_canonical(hotkey.press),
    on_release=for_canonical(hotkey.release))
listener.start()
# Порождение
[item.start() for item in threads]

# Заполнение очереди живыми и готовыми потоками
for thread in threads:
    print(2)
    if thread.is_ready() and thread.is_alive():
        ready_queue.put(thread)

# Основная логика программы
while True:
    print("_________________________________________________________")
    print("Готовность: ", [i.name for i in ready_queue.queue])
    print("Ожидание: ", [i.name for i in wait_queue.queue])
    print()
    active_thread = ready_queue.get()
    active_thread.resume()
    Lllecmepka.set_active_thread(active_thread)
    wait_for_tick_expire(active_thread)
    active_thread.pause()
    Lllecmepka.set_active_thread(None)
    if active_thread.is_ready():
        ready_queue.put(active_thread)
    # ready_queue.put(active_thread)


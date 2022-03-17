import threading
from threading import Thread, Event
import time
import itertools
from string import ascii_letters
from queue import Queue

MIN_LEN = 5
MAX_LEN = 26
QUANTUM = 0.045  # sec
WORDS = ("BEttA", "glADE", "BrUTE")

ready_queue = Queue(maxsize=3)
tick = 12*QUANTUM


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
        # print(f"Thread '{self.name}' was born!")
        self.__is_ready = True
        if self._simple_brute() is not None:
            print(f"Thread '{self.name}' successfully completed! Word: {self.word} Combinations: {self.__count}")
        else:
            print(f"Thread '{self.name}' unsuccessfully finished! Word: {self.word} Combinations: {self.__count}")

    def pause(self):
        if self.is_alive():
            # print(f"Thread '{self.name}' paused")
            self.__pause_event.clear()

    def resume(self):
        if not self.__pause_event.is_set():
            # print(f"Thread '{self.name}' resumed")
            self.__pause_event.set()

    def is_ready(self):
        return self.__is_ready


threads = [BruteThread("Foo()", WORDS[0]), BruteThread("Bar()", WORDS[1]), BruteThread("Baz()", WORDS[2])]

# Порождение
[item.start() for item in threads]

# Заполнение очереди живыми и готовыми потоками
for thread in threads:
    if thread.is_ready() and thread.is_alive():
        ready_queue.put(thread)

# Основная логика программы
while True:
    thread = ready_queue.get()
    thread.resume()
    time.sleep(tick)
    thread.pause()
    ready_queue.put(thread)

# while True:
#
#
#
#
#
# while True:
#     for item in q:
#         print(time.thread_time())
#         item.resume()
#         time.sleep(5)
#         item.pause()
# one.start()
# while True:x`x`
#     one.pause()
#     time.sleep(0.1)
#     one.resume()
#     time.sleep(15)

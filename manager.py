import threading
import time
import itertools
from string import ascii_letters

MIN_LEN = 1
MAX_LEN = 26
tasks = ("BEttA", "glADE", "BrUTE")

condition = threading.Condition()


class BruteThread(threading.Thread):
    def __init__(self, name, word):
        threading.Thread.__init__(self)
        self.name = name
        self.word = word
        self.__count = 0
        self.__pause_event = threading.Event()
        self.__pause_event.set()

    def _simple_brute(self):
        for repeat in range(MIN_LEN, MAX_LEN):
            for i in itertools.product(ascii_letters, repeat=repeat):
                self.__count += 1
                self.__pause_event.wait()
                print(i)
                if ''.join(i) == self.word:
                    return True
        return None

    def run(self):
        print(self.name)
        if self._simple_brute() is not None:
            print(f"Thread '{self.name}' successfully completed! Word: {self.word} Combinations: {self.count}")
        else:
            print(f"Thread '{self.name}' unsuccessfully finished! Word: {self.word} Combinations: {self.count}")

    def pause(self):
        self.__pause_event.clear()

    def resume(self):
        self.__pause_event.set()


one = BruteThread("one", tasks[0])
two = BruteThread("two", tasks[1])
three = BruteThread("three", tasks[2])

one.start()
while True:
    one.pause()
    time.sleep(5)
    one.resume()
    time.sleep(2)



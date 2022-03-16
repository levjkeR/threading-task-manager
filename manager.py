import threading
import time
import itertools
from string import ascii_letters

MIN_LEN = 1
MAX_LEN = 26
tasks = ("BEttA", "glADE", "BrUTE")


class BruteThread(threading.Thread):
    def __init__(self, name, word):
        threading.Thread.__init__(self)
        self.name = name
        self.word = word
        self.count = 0

    def _simple_brute(self):
        for repeat in range(MIN_LEN, MAX_LEN):
            for i in itertools.product(ascii_letters, repeat=repeat):
                self.count += 1
                if ''.join(i) == self.word:
                    return True
        return None

    def run(self):
        if self._simple_brute() is not None:
            print(f"Thread '{self.name}' successfully completed! Word: {self.word} Combinations: {self.count}")
        else:
            print(f"Thread '{self.name}' unsuccessfully finished! Word: {self.word} Combinations: {self.count}")


# locker = threading.RLock()  # The class implementing primitive lock objects
for w in tasks:
    thread = BruteThread(w, w)
    thread.start()

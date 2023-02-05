import logging
import time
import concurrent.futures
import threading

class MultithreadedHash:
    def __init__(self, request):
        self.letter = None
        self.lock = threading.Lock()
        self.letters = None
        self.value = 0
        self.request = request
        self.current_letter = None


    def get_next(self, letters):

        with self.lock:
            self.letters = letters
            print("has lock", letters)
            # print("Thread %s: pre-increment - local_copy %d self.value %d", name, local_copy, self.value)
            # print("Thread %s: post-increment - local_copy %d self.value %d", name, local_copy, self.value)
            # print("Thread %s sleep", name)
            # print("Thread %s: assign to self.value - local_copy %d self.value %d", name, local_copy, self.value)
            # print("Thread %s about to release lock", name)
        # self._lock.release() # manually release lock
        # print("Thread %s after release", name)
        # print("Thread %s: finishing update", name)

def main():
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=print,
                        datefmt="%H:%M:%S")

    threads = MultithreadedHash()
    print("Testing update. Starting value is %d.", 4)
    # create two threads, where both have equal access to the threads
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        for index in range(4):
            executor.submit(threads.update, index)
    print("Testing update. Ending value is %d.", threads.value)


if __name__ == '__main__':
    main()
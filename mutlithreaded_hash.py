import logging
import time
import concurrent.futures
import threading
import string

class MultithreadedHash:

    def __init__(self, request):
        self.letter = None
        self.letters = None
        self.value = 0
        self.request = request
        self.alphabets_iter = iter(list(string.ascii_letters))
        self.END_OF_ALPHABETS = 'Z'

        

    # def get_next(self):
    #     try:
    #         next(self.alphabets_iter)
    #     except StopIteration as e:
    #         self.alphabets_iter = iter(list(string.ascii_letters))

    
    def init_crack(self, letters):
        for letter in letters:
            if letter == self.END_OF_ALPHABETS:
                print('end')
            

    

    def process_request(self, letter):        
        
        # hash_guesser.crack_hash(list(string.ascii_letters), letters_length)

        with self.lock:
            print('locking', letter)
            self.letters = letter
            self.init_crack(letter)
            


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
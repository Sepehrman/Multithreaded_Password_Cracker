import crypt
import threading

class HashGuesser:

    def __init__(self):
        self.username = None
        self.hashed = None
        self.id = None
        self.salt = None
        self.last_updated = None
        self.hashed_password = None
        self.cracked_password = None
        self.hashing_type = None
        self.tries = 0
        self.time_taken = None

    def __str__(self):
        return f'"{self.username}" is using the "{self.hashing_type}" hashing algorithm.\n' \
               f'Cracked Password: "{self.cracked_password}"\n' \
               f'Number of trials: {self.tries}\n' \
               f'Time taken: {self.time_taken:.6f} (seconds)\n'

    def crack_hash(self, char_list, n, empty_list=[]):
        guess = crypt.crypt(''.join(empty_list), self.hashed_password)
        self.tries += 1
        if guess == self.hashed_password:
            self.cracked_password = ''.join(empty_list)

        if len(empty_list) == n:
            pass
        else:
            for c in char_list:
                if self.cracked_password is not None:
                    return True
                self.crack_hash(char_list, n, empty_list + [c])

    def identify_hash(self):
        self.hashing_type = 'N/A'
        if self.hashed_password.startswith('$1$'):
            self.hashing_type = 'MD5'
        elif self.hashed_password.startswith('$2a$'):
            self.hashing_type = 'Blowfish'
        elif self.hashed_password.startswith('$2y$'):
            self.hashing_type = 'Blowfish'
        elif self.hashed_password.startswith('$5$'):
            self.hashing_type = 'SHA-256'
        elif self.hashed_password.startswith('$6$'):
            self.hashing_type = 'SHA-512'
        elif self.hashed_password.startswith('$y$'):
            self.hashing_type = 'yescrypt'

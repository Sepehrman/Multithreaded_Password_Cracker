import argparse
import string
import time
import concurrent.futures
import warnings
import multiprocessing
from mutlithreaded_hash import MultithreadedHash
from request import Request
from hash_guesser import HashGuesser

with warnings.catch_warnings():
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    import crypt


def define_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', help='The shadow file we want to crack the password of.')
    parser.add_argument('users', nargs='*', help="Argument with no flag that is a list of usernames")
    parser.add_argument("-t", "--threads", help=f"The number of threads we would like to run the program on. "
                                                "Defaults to the current machine's number of CPU Cores",
                        default=multiprocessing.cpu_count())

    request = Request()
    args = parser.parse_args()
    request.file = args.file
    request.users = args.users
    request.threads = int(args.threads)

    
    if (len(request.users) == 0 or request.users is None) and request.file is None:
        print("Must include the following argument -f/--file and must include usernames")
        quit()

    if len(request.users) == 0 or request.users is None:
        print("Must include username(s)")
        quit()

    if request.file is None:
        print("Must include a shadow fie to look at the hash")
        quit()


    print(request)

    return request


def extract_etc_shadow(hashed_line):
    info_array = hashed_line.split(":")
    hash_details = info_array[1][1:].split('$')

    hash_guess = HashGuesser()
    hash_guess.username = info_array[0]
    hash_guess.id = hash_details[0]

    hash_guess.salt = hash_details[1]
    hash_guess.hashed = hash_details[2]
    hash_guess.last_updated = info_array[2]
    hash_guess.hashed_password = info_array[1]
    hash_guess.identify_hash()
    return hash_guess


def find_lines_from_user(req: Request, username):
    with open(req.file, "r") as file:
        lines = file.readlines()
        for line in lines:
            if line.startswith(username):
                return line
    print(f"*** Warning: '{username}' is not associated with this file. Cannot crack password. ***")


def find_lines(request, hashed_lines):
    for user in request.users:
        found = find_lines_from_user(request, user)
        if found:
            hashed_lines.append(found)
    if len(hashed_lines) == 0:
        print("!!! Error: None of the usernames provided are available within the shadow file. Please check the "
              "usernames. !!!")
        quit()


def generate_guessers(hashed_lines, guessers):
    for hashed_line in hashed_lines:
        guessers.append(extract_etc_shadow(hashed_line))


def partition_letters(a, n):
        k, m = divmod(len(a), n)
        return (a[i*k+min(i, m):(i+1)*k+min(i+1, m)] for i in range(n))


def start_cracking(guessers: list[HashGuesser]):
    print("Cracking Process initiated..,")
    print("----------------RESULTS----------------")
    letters_length = 1
    for hash_guesser in guessers:
        start = time.time()
        while hash_guesser.cracked_password is None:
            hash_guesser.crack_hash(list(string.ascii_letters), letters_length)
            letters_length += 1
        elapsed = time.time()
        hash_guesser.time_taken = elapsed - start
        letters_length = 1
        print(hash_guesser)


def thread_function(letters):
    print(f"ALL {letters}")

def main():
    request = define_arguments()
    hashed_lines = []
    guessers = []

    find_lines(request, hashed_lines)
    generate_guessers(hashed_lines, guessers)
    partitioned_letters = partition_letters(list(string.ascii_letters), request.threads)

    multithreads = MultithreadedHash(request)
    
    
    # ADD '' TO START OF ALL ELEMENTS WHEN STARTING, THEN add a, then b, then c to the start
    with concurrent.futures.ThreadPoolExecutor(max_workers=request.threads) as executor:
        for index in partitioned_letters:
            # PARTITIONING 4 THREADS (Order in which they print doesn't matter)
            executor.submit(multithreads.get_next, index)

    # start_cracking(guessers)


if __name__ == '__main__':
    main()





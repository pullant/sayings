import csv

from build_queue import build_queue
import config

INFO = config.INFO
QUEUE = config.QUEUE
PHRASES = config.PHRASES
fieldnames = ['ID', 'date', 'days', 'phrase']
# next ID = last 'ID' in PHRASES + 1


def main():

    while True:
        response = input("""
╭─────────┬──────────┬────────╮
│ [w]rite │ [r]eview │ [q]uit │
├─────────┴──────────┴────────╯
╰──> """)
        if response == 'w':
            write_phrase()
        elif response == 'r':
            review_phrase()
        elif response == 'q':
            print()
            break


def write_phrase():

    # CALL QUEUE builder
    today = build_queue()

    # APPEND new entry to PHRASES
    with PHRASES.open('a+', newline='') as phrases:
        writer = csv.DictWriter(phrases, fieldnames=fieldnames)

        # get new phrase
        phrase = input('\nphrase // ')

        # get last ID in PHRASES
        # check if PHRASES was just created and add headers
        phrases.seek(0) # back to beginning of phrases
        if phrases.readline() == '':
            writer.writeheader()
            ID = '0' # set first ID

            # readline() moved the stream position to the next line
            # the characters of the first line plus the newline characters
            # (\r\n or \n) (ID,date,days,phrase = 19)
            # total from 0 to 21 use phrases.tell() to check

        elif phrases.readline() == '': # check if PHRASES has headers but it is empty
            ID = '0' # set new first ID

        else:
            phrases.seek(0) # back to beginning of phrases
            # get last ID and set stream to the end of the file to append new phrase
            ID = phrases.readlines()[-1].strip().split(',')[0]
            ID = int(ID) + 1

        # append entry
        writer.writerow({'ID': ID, 'date': today, 'days': '1', 'phrase': phrase})

        # because readlines() moved the stream to the end of the file
        # writerow() will work as append

    # APPEND new entry to QUEUE
    with QUEUE.open('a+', newline='') as queue:
        writer = csv.DictWriter(queue, fieldnames=fieldnames)

        # check if QUEUE was just created and add headers
        queue.seek(0) # back to beginning of queue
        if queue.readline() == '':
            writer.writeheader()

        # otherwise append entry
        queue.seek(0, 2) # back to end of queue
        writer.writerow({'ID': ID, 'date': today, 'days': '1', 'phrase': phrase})


def review_phrase():
    return


if __name__ == "__main__":
    main()


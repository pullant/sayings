import csv
from datetime import date

import config
INFO = config.INFO
QUEUE = config.QUEUE
PHRASES = config.PHRASES
fieldnames = ['ID', 'date', 'days', 'phrase']


# FIRST RUN
# - create INFO done by config.py
# - no QUEUE to build
# RUNNING
# - get last_queue_update date from INFO
# - compare it to today
# same:
#    do nothing QUEUE built by write.py
# different:
#    build QUEUE from (last_queue_update + 1) to (date.today)
#    set last_queue_update to date.today

def build_queue():

    today = date.today().strftime('%Y%m%d')

    # first run PHRASES DOES NOT EXIST yet
    # neither does QUEUE, no queue to build
    if not PHRASES.exists() or not QUEUE.exists():
        return today

    # if QUEUE is empty
    # - no QUEUE to build
    # - or days have passed and now there is a QUEUE to build
    if QUEUE.read_text().split('\n')[1] == '':
        last_queue_update = INFO.read_text().split('\n')[1]

    # there is a QUEUE
    # date of last entry in QUEUE is last_queue_update
    else:
        with QUEUE.open('r', newline='') as queue:
            last_queue_update = queue.readlines()[-1].strip().split(',')[1]

    # RUNNING
    # Get from PHRASES all the entries that have
    # a date between (last_queue_update + 1 ) and (today)
    # Append them to QUEUE in order 1 day at a time
    with PHRASES.open('r', newline='') as phrases:
        phrases_reader = csv.DictReader(phrases)
        with QUEUE.open('a', newline='') as queue:
            queue_writer = csv.DictWriter(queue, fieldnames=fieldnames)

            # Have to add entries in order since the queue is taking from the top
            # Number of times to go over PHRASES to add the phrases one day at a time = today - last_queue_update
            for times in range(int(today) - int(last_queue_update)):
                last_queue_update = int(last_queue_update) + 1
                for entry in phrases_reader:
                    if int(entry['date']) == last_queue_update:
                        queue_writer.writerow(entry)
                phrases.seek(0) # back to the beginning of PHRASES
                next(phrases) # skip top row header

    # update INFO
    INFO.write_text(f'last_queue_update\n{today}\n')

    return today


if __name__ == "__main__":
    main()


import csv
from shutil import copy

import config

QUEUE = config.QUEUE
PHRASES = config.PHRASES
queue_temp = config.queue_temp
phrases_temp = config.phrases_temp
fieldnames = ['ID', 'date', 'days', 'phrase']


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


def review_phrase():

    if not QUEUE.exists():
        print('\n' + 'Nothing to review.')
        return

    while True:

        today = build_queue()

        queue = QUEUE.open('r', newline='')
        reader = csv.DictReader(queue)
        for entry in reader:
            print('\n' + '  “ ' + entry['phrase'] + ' ”')
            break
        else:
            print('\n' + 'Review done!')
            queue.close()
            return

        response = input("""
╭────────┬────────┬─────────┬──────────┬────────╮
│ [e]asy │ [h]ard │ [a]gain │ [d]elete │ [q]uit │
├────────┴────────┴─────────┴──────────┴────────╯
╰──> """)
        if response == "e":
            easy_phrase(entry, today)
        elif response == "h":
            hard_phrase(entry, today)
        elif response == "a":
            again_phrase(entry, today)
        elif response == "d":
            delete_entry(entry, today)
        elif response == "q":
            break

    queue.close()
    return


def delete_entry(entry, today):

    # UPDATE entry in PHRASES
        # read phrases
            # if ID is ID of entry
                # write updated entry with new date and days added to phrases_temp
            # else write entry to phrases_temp
        # copy phrases_temp to phrases.csv
    with PHRASES.open('r', newline='') as phrases:
        reader = csv.DictReader(phrases)
        with phrases_temp.open('w', newline='') as temp:
            writer = csv.DictWriter(temp, fieldnames=fieldnames)
            writer.writeheader()
            for row in reader:
                if row['ID'] == entry['ID']:
                    # skip it
                    continue
                else:
                    writer.writerow(row)
    copy(phrases_temp, PHRASES)

    # REMOVE entry from QUEUE
    # remove top entry in QUEUE
    with QUEUE.open('r', newline='') as queue:
        reader = csv.DictReader(queue, fieldnames=fieldnames)
        with queue_temp.open('w', newline='') as temp:
            writer = csv.DictWriter(temp, fieldnames=fieldnames)
            next(queue) # skip header
            next(queue) # skip first row
            writer.writeheader()
            for row in reader:
                writer.writerow(row)
    copy(queue_temp, QUEUE)


def easy_phrase(entry, today):
    return


def hard_phrase(entry, today):
    return


def again_phrase(entry, today):
    return


def write_phrase():
    return


if __name__ == "__main__":
    main()

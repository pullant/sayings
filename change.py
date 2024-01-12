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
╭────────┬────────┬─────────┬──────────┬──────────┬────────╮
│ [e]asy │ [h]ard │ [a]gain │ [c]hange │ [d]elete │ [q]uit │
├────────┴────────┴─────────┴──────────┴──────────┴────────╯
╰──> """)
        if response == "e":
            easy_phrase(entry, today)
        elif response == "h":
            hard_phrase(entry, today)
        elif response == "a":
            again_phrase(entry, today)
        elif response == "c":
            change_phrase(entry, today)
        elif response == "d":
            delete_entry(entry, today)
        elif response == "q":
            break

    queue.close()
    return


def change_phrase(entry, today):

    # get new phrase
    phrase = input('\nphrase // ')

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
                    row['phrase'] = phrase
                    writer.writerow(row)
                else:
                    writer.writerow(row)
    copy(phrases_temp, PHRASES)

    with QUEUE.open('r', newline='') as queue:
        reader = csv.DictReader(queue, fieldnames=fieldnames)
        with queue_temp.open('w', newline='') as temp:
            writer = csv.DictWriter(temp, fieldnames=fieldnames)
            next(queue) # skip header
            next(queue) # skip first row
            writer.writeheader()
            for row in reader:
                writer.writerow(row)
            writer.writerow({'ID': entry['ID'], 'date': entry['date'], 'days': entry['days'], 'phrase': phrase})
    copy(queue_temp, QUEUE)


def easy_phrase(entry, today):
    return


def hard_phrase(entry, today):
    return


def again_phrase(entry, today):
    return

def delete_entry(entry, today):
    return

def write_phrase():
    return


if __name__ == "__main__":
    main()

import csv
from datetime import datetime, timedelta
from shutil import copy

from build_queue import build_queue
import config

INFO = config.INFO
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

    # CHECK if QUEUE exist
    # if it does not exist return home "Nothing to review."
    if not QUEUE.exists():
        print('\n' + 'Nothing to review.')
        return

    # SET review mode
    while True:

        # CALL QUEUE builder
        today = build_queue()

        # GET first entry from QUEUE
        queue = QUEUE.open('r', newline='')
        reader = csv.DictReader(queue)
        for entry in reader:
            print('\n' + '  “ ' + entry['phrase'] + ' ”')
            break
            # break out of the loop because if it finishes,
            # it will execute the else statement
        # if QUEUE is empty return home
        else:
            print('\n' + 'Review done!')
            queue.close()
            return # go home
            # if there is no row the loop will finish
            # and the else statement will be executed

        # ASK the user to qualify the phrase
        response = input("""
╭────────┬────────┬─────────┬────────╮
│ [e]asy │ [h]ard │ [a]gain │ [q]uit │
├────────┴────────┴─────────┴────────╯
╰──> """)
        # update entry according to user input or quit
        if response == "e":
            easy_phrase(entry, today)
        elif response == "h":
            hard_phrase(entry, today)
        elif response == "a":
            again_phrase(entry, today)
        elif response == "q":
            break

    queue.close()
    return # go home


def easy_phrase(entry, today):

    # days for easy = days added last time * 2
    days_to_next_review = int(entry['days']) * 2

    update_entry(entry, days_to_next_review, today)


def hard_phrase(entry, today):

    # days for hard = days for easy / 2 = days added last time
    days_to_next_review = int(entry['days'])

    update_entry(entry, days_to_next_review, today)


def update_entry(entry, days_to_next_review, today):

    # GET new date for entry
    # entry['date'] = today
    # - not reviewed older entries in the queue are going to be reviewed
    # as if they were added today
    # - so the next review is going to be scheduled counting from today

    # new date = date + days to next review
    new_date = datetime.strptime(today, '%Y%m%d') + timedelta(days=days_to_next_review)
    new_date = new_date.strftime('%Y%m%d')

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
                    row['days'] = days_to_next_review
                    row['date'] = new_date
                    writer.writerow(row)
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


def again_phrase(entry, today):

    # MOVE entry to the end of QUEUE
    with QUEUE.open('r', newline='') as queue:
        reader = csv.DictReader(queue, fieldnames=fieldnames)
        with queue_temp.open('w', newline='') as temp:
            writer = csv.DictWriter(temp, fieldnames=fieldnames)

            # read QUEUE from the second row forward
            next(queue) # skip header
            next(queue) # skip first row in QUEUE

            # write it to queue_temp
            writer.writeheader()
            for row in reader:
                writer.writerow(row)

                # if the reader is used
                # - after the stream was moved (next(queue))
                # - and no fieldnames were given
                # the reader takes the data in the new position as
                # the key values for the dictionary been created
                # solution:
                # - add the fieldnames to the reader
                # - and then move stream as necessary

            # update date of entry and write it to the end
            entry['date'] = today
            writer.writerow(entry)

    copy(queue_temp, QUEUE)


def write_phrase():
    return


if __name__ == "__main__":
    main()

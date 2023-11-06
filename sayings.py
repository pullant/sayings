# python3 ./sayings.py
# Python 3.12.0

import config
from review import review_phrase
from write import write_phrase


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


if __name__ == "__main__":
    main()

from datetime import date
from pathlib import Path

# import config
# - the first time the import statement is encountered
# the code in config.py is executed.
# - variables, functions, and classes defined in config.py
# become attributes of the config module.

# set absolute paths to data/* and create data/ if does not exists
p = Path(__file__) # path to this file
p.parent.joinpath('data').mkdir(exist_ok=True) # if dir exist no error
INFO = p.parent / 'data' / 'info.csv'
QUEUE = p.parent / 'data' / 'queue.csv'
PHRASES = p.parent / 'data' / 'phrases.csv'
queue_temp = p.parent / 'data' / 'queue_temp'
phrases_temp = p.parent / 'data' / 'phrases_temp'

# FIRST RUN of the program I need to have INFO
# for last_queue_update since is data that has to be persistent
# or I could look it up in PHRASES (smallest date)
if not INFO.exists():
    # set it to today since it is the first run
    todayI = date.today().strftime('%Y%m%d')
    INFO.write_text(f'last_queue_update\n{todayI}\n')


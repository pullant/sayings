from datetime import date
from pathlib import Path

# set absolute paths to data/* and create data/ if it does not exists
p = Path(__file__) # path to this file
p.parent.joinpath('data').mkdir(exist_ok=True)
INFO = p.parent / 'data' / 'info.csv'
QUEUE = p.parent / 'data' / 'queue.csv'
PHRASES = p.parent / 'data' / 'phrases.csv'
queue_temp = p.parent / 'data' / 'queue_temp'
phrases_temp = p.parent / 'data' / 'phrases_temp'

# FIRST RUN
# - create INFO
# - set last_queue_update to date.today
if not INFO.exists():
    today = date.today().strftime('%Y%m%d')
    INFO.write_text(f'last_queue_update\n{today}\n')


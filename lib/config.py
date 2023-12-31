import os


WORK_DIR = os.getenv('PYTHONPATH')
LOGS_FILE = os.path.join(WORK_DIR, 'bin', 'logs.txt')
STATE_FILE = os.path.join(WORK_DIR, 'bin', 'state')


class Jobs:
    class DumpState:
        interval = 40
        first = 40
    
    class ShowActualHabits:
        interval = 60
        first = 60

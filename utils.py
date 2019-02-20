import time
import numpy as np


def truncate(n, decimals=0):
    multiplier = 10 ** decimals
    return int(n * multiplier) / multiplier


def print_header(col_width, columns):
    print(("+" + "-" * col_width) * len(columns) + "+")
    columns_row = ""
    for column in columns:
        columns_row += "|" + column.center(col_width, " ")
    print(columns_row + "|")
    print(("+" + "=" * col_width) * len(columns) + "+")


def print_row(cell_width, cells):
    row = ""
    for cell in cells:
        row += "|" + cell.center(cell_width, " ")
    print(row + "|")
    print(("+" + "-" * cell_width) * len(cells) + "+")


def format_percentage(percentage):
    return format(percentage, '.2f') + "%"


timeblocks = {}
timings_active = False


class TimeBlock:

    def __init__(self, name):
        self.start = time.time()
        self.name = name.rjust(15, ' ')

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        end = time.time()
        runtime = int((end - self.start) * 1000)
        runtime_str = str(runtime).rjust(4, ' ')
        msg = '{name} took {time} ms'
        if self.name not in timeblocks:
            timeblocks[self.name] = []
        timeblocks[self.name].append(runtime)
        if timings_active:
            print(msg.format(time=runtime_str, name=self.name))


def timeblock_stats():
    for name, timings in timeblocks.items():
        count = str(len(timings)).rjust(5, ' ')
        min = str(np.min(timings)).rjust(4, ' ')
        max = str(np.max(timings)).rjust(4, ' ')
        avg = str(int(np.average(timings))).rjust(4, ' ')
        print(f'{name} happened {count} fastest: {min}ms slowest: {max}ms avg: {avg}ms')

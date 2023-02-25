import functools
import pprint
import string
import time
from typing import Optional


class reversor:
    def __init__(self, obj):
        self.obj = obj

    def __eq__(self, other):
        return other.obj == self.obj

    def __lt__(self, other):
        return other.obj < self.obj


pp = pprint.PrettyPrinter().pprint


def convert_runtime(runtime: int) -> str:
    return f"{int(runtime / 60)}:{(runtime % 60):02d}"


def strip_all_punctuation(subject: str) -> str:
    # add "smart quotes" that Notion uses
    punctuation = string.punctuation + "“‘”’"
    return subject.translate(str.maketrans("", "", punctuation))


def measure_execution(description: Optional[str] = None):
    def wrap(func):
        @functools.wraps(func)
        def wrapped_f(*args, **kwargs):
            start_time = time.time()
            if description:
                print(description)
            res = func(*args, **kwargs)
            print(f"Took {time.time() - start_time} seconds")
            return res

        return wrapped_f

    return wrap

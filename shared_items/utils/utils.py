import functools
import pprint
import string
import time
from typing import Optional

TAB = "\t"


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
            start_time = time.monotonic()
            if description:
                print(description)
            res = func(*args, **kwargs)
            print(f"{TAB}Took {time.monotonic() - start_time} seconds\n")
            return res

        return wrapped_f

    return wrap


def try_it(func):
    name = func.__name__

    @functools.wraps(func)
    def wrapped_f(*args, **kwargs):
        try:
            print(f"STARTING {name}")
            return func(*args, **kwargs)
        except Exception:
            import traceback

            print()
            print("----------------------------------------------------")
            print(f"------------- error in {name} -------------")
            print("----------------------------------------------------")
            print()
            traceback.print_exc()

    return wrapped_f

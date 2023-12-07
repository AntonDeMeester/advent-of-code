from importlib import import_module
from os import listdir
from os.path import isfile
from time import time


def exec():
    onlyfiles = sorted(f for f in listdir(".") if isfile(f) and f.endswith(".py") and not f.startswith("00"))
    total = []
    for f in onlyfiles:
        start = time()
        import_module(f[:-3])
        end = time()
        total.append(f"{f} took {(end-start) * 1000:.2f}ms")

    [print(t) for t in total]


exec()

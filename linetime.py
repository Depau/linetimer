#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import subprocess
import sys
import warnings
from datetime import datetime
from io import BytesIO
from select import select
from typing import cast


class Colors:
    """ ANSI color codes """
    BLACK = "\033[0;30m"
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    BROWN = "\033[0;33m"
    BLUE = "\033[0;34m"
    PURPLE = "\033[0;35m"
    CYAN = "\033[0;36m"
    LIGHT_GRAY = "\033[0;37m"
    DARK_GRAY = "\033[1;30m"
    LIGHT_RED = "\033[1;31m"
    LIGHT_GREEN = "\033[1;32m"
    YELLOW = "\033[1;33m"
    LIGHT_BLUE = "\033[1;34m"
    LIGHT_PURPLE = "\033[1;35m"
    LIGHT_CYAN = "\033[1;36m"
    LIGHT_WHITE = "\033[1;37m"
    BOLD = "\033[1m"
    FAINT = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"
    BLINK = "\033[5m"
    NEGATIVE = "\033[7m"
    CROSSED = "\033[9m"
    END = "\033[0m"


def main() -> int:
    if len(sys.argv) <= 1:
        print("Times stdout/stderr lines of a subprocess relative from start time.")
        print(f"Usage: {sys.argv[0]} [command] [args...]")
        return 1

    t0 = datetime.now()

    p = subprocess.Popen(sys.argv[1:], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=sys.stdin)
    pout = p.stdout
    perr = p.stderr
    fds = [pout, perr]

    while not p.poll() and fds:
        r, w, x = select(fds, [], fds)

        if x:
            warnings.warn(f"Exceptional conditions: {x}")
            for fd in x:
                fds.remove(fd)
                fd.close()

        t1 = datetime.now()
        delta = t1 - t0

        for fd in r:
            try:
                fd = cast(BytesIO, fd)

                line = fd.readline()
                if not line:
                    fds.remove(fd)
                    fd.close()
                    continue

                prefix = "out"
                if fd.fileno() == perr.fileno():
                    prefix = "err"

                print(Colors.LIGHT_GRAY + f"[{prefix} {str(delta):>14}]" + Colors.END, line.decode(errors='replace'),
                      end='')
            except ValueError as e:
                if 'I/O operation on closed file' in str(e):
                    fds.remove(fd)
                else:
                    raise

    return p.wait()


if __name__ == '__main__':
    sys.exit(main())

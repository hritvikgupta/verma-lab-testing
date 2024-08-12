from __future__ import annotations

import argparse
from typing import Sequence
import logging
import sys
import os

# Add the directory of this script to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from .utils import added_files


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    
    parser.add_argument(
        'filenames', nargs='*',
        help='Filenames pre-commit believes are changed.',
    )
    parser.add_argument(
        '--enforce-all', action='store_true',
        help='Enforce all files are checked, not just staged files.',
    )

    args = parser.parse_args(argv)
    retv = 0

    if not args.enforce_all:
        args.filenames &= added_files()

    binary_files = []

    # Characters that are used in text
    textchars = bytearray({7,8,9,10,12,13,27} | set(range(0x20, 0x100)) - {0x7f})

    # Lambda function to check if a file is a binary file
    is_binary_string = lambda bytes: bool(bytes.translate(None, textchars))

    for filename in args.filenames:
        with open(filename, 'rb') as f:
            if is_binary_string(f.read(1024)):
                binary_files.append(filename)

    if(binary_files):
        for binary_file in binary_files:
            print(f'Binary file found: {binary_file}')
        retv = 1

    return retv

    


if __name__ == '__main__':
    logging.basicConfig(filename='pre_commit.log', level=logging.INFO)
    raise SystemExit(main())

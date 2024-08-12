from __future__ import annotations

import argparse
from typing import Sequence
import logging
import sys
import os
from utils import added_files


def find_string_in_files(
        filenames: Sequence[str],
        search_string: str,
        *,
        enforce_all: bool = False,
        case_insensitive: bool = False,
        quiet_skip_binary: bool = False,
) -> int:
    # Find all files in the list of files pre-commit tells us about
    # and check if they contain a search_string using grep
    retv = 0
    bad_files = []

    filenames_filtered = set(filenames)

    if not enforce_all:
        filenames_filtered &= added_files()

    for filename in filenames_filtered:
        with open(filename, 'r') as f:
            try:
                content = f.read()
                if case_insensitive:
                    content = content.lower()
                if search_string in content:
                    bad_files.append(filename)
                    # TODO: consider reporting line number and line itself
            
            except UnicodeDecodeError:
                if not quiet_skip_binary:
                    print(f'File {filename} is not a plaintext file, skipping...')

    if bad_files:
        for bad_file in bad_files:
            print(f'Search string {search_string} found in: {bad_file}')
        retv = 1

    return retv


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
    parser.add_argument(
        '--search-string', type=str, default=None,
        help='String to search for in the files.',
    )
    parser.add_argument(
        '--case-insensitive', action='store_true',
        help='Make search string case insensitive.',
    )
    parser.add_argument(
        '--quiet-skip-binary', action='store_true',
        help='Skip binary files with no reporting (otherwise will report that the file was skipped).',
    )
    args = parser.parse_args(argv)

    if args.case_insensitive:
        args.search_string = args.search_string.lower()

    return find_string_in_files(
        args.filenames,
        args.search_string,
        enforce_all=args.enforce_all,
        case_insensitive=args.case_insensitive,
        quiet_skip_binary=args.quiet_skip_binary,
    )


if __name__ == '__main__':
    logging.basicConfig(filename='pre_commit.log', level=logging.INFO)
    raise SystemExit(main())

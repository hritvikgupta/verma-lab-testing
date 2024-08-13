from __future__ import annotations

import argparse
from typing import Sequence
import logging
import sys
import os
from utils import added_files

# Setup logging
logging.basicConfig(filename='pre_commit.log', level=logging.INFO)
logger = logging.getLogger(__name__)

def find_string_in_files(
        filenames: Sequence[str],
        search_string: str,
        *,
        enforce_all: bool = False,
        case_insensitive: bool = False,
        quiet_skip_binary: bool = False,
) -> int:
    retv = 0
    bad_files = []

    filenames_filtered = set(filenames)

    if not enforce_all:
        filenames_filtered &= added_files()

    for filename in filenames_filtered:
        logger.info(f"Processing file: {filename}")
        try:
            with open(filename, 'r') as f:
                content = f.read()
                if case_insensitive:
                    content = content.lower()
                if search_string in content:
                    bad_files.append(filename)
                    logger.info(f"Found '{search_string}' in file: {filename}")
            
        except UnicodeDecodeError:
            if not quiet_skip_binary:
                logger.info(f'File {filename} is not a plaintext file, skipping...')
                print(f'File {filename} is not a plaintext file, skipping...')

    if bad_files:
        for bad_file in bad_files:
            logger.info(f"Search string '{search_string}' found in: {bad_file}")
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
    raise SystemExit(main())

from __future__ import annotations

import argparse
from typing import Sequence
import logging
from custom_precommit_hooks.utils import added_files

container_definers = [
    'process.container = ',
]

container_str_required_defaults = [
    "process.container = 'PATH/TO/CONTAINER'"
]

def check_container_defs(
        filenames: Sequence[str],
        *,
        enforce_all: bool = False,
        quiet_skip_binary: bool = False,
) -> int:
    # Find all files in the list of files pre-commit tells us about
    # and check if they contain a search_string using grep
    retv = 0
    bad_files = []
    diff_defs = []

    filenames_filtered = set(filenames)

    if not enforce_all:
        filenames_filtered &= added_files()

    for filename in filenames_filtered:
        with open(filename, 'r') as f:
            try:
                content = f.read()

                n_cont_definitions = sum([content.count(container_definer) for container_definer in container_definers])
                n_cont_default_correct = sum([content.count(container_str) for container_str in container_str_required_defaults])

                if n_cont_default_correct != n_cont_definitions:
                    bad_files.append(filename)
                    diff_defs.append(n_cont_definitions - n_cont_default_correct)
            
            except UnicodeDecodeError:
                if not quiet_skip_binary:
                    print(f'File {filename} is not a plaintext file, skipping...')

    if bad_files:
        for i, bad_file in enumerate(bad_files):
            print(f'{bad_file} has {diff_defs[i]} container definition(s) without default (such as {container_str_required_defaults[0]}).')
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
        '--quiet-skip-binary', action='store_true',
        help='Skip binary files with no reporting (otherwise will report that the file was skipped).',
    )
    args = parser.parse_args(argv)

    return check_container_defs(
        args.filenames,
        enforce_all=args.enforce_all,
        quiet_skip_binary=args.quiet_skip_binary,
    )


if __name__ == '__main__':
    logging.basicConfig(filename='pre_commit.log', level=logging.INFO)
    raise SystemExit(main())

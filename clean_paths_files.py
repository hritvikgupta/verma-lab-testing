import re
import argparse
from typing import Sequence

def clean_files(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()

        pattern = r'"\/path\/to\/file_param_name\.extension?"'
        replacement = '"dummy/file_param_name.extension"'

        cleaned_files = re.sub(pattern, replacement, content)

        with open(file_path, 'w') as file:
            file.write(cleaned_files)
    except Exception as e:
        print(f"An Error Occured :{e}")
    
def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs = '*', help='filenames to clean')
    args = parser.parse_args(argv)
    for file_path in args.filenames:
        clean_files(file_path)
    
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())

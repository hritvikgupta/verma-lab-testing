import re
import os
import argparse

def clean_file(file_path):
    print(f"Cleaning file: {file_path}")
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # Define the pattern and replacement
        pattern = r'dummy/file_param_name.extension'
        replacement = 'dummy/file_param_name.extension'

        # Perform the replacement
        cleaned_content = re.sub(pattern, replacement, content)

        if content != cleaned_content:
            # Write the cleaned content back to the file
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(cleaned_content)
            print(f"File modified: {file_path}")
        else:
            print(f"No changes needed for file: {file_path}")

    except Exception as e:
        print(f"Error cleaning file: {e}")

def clean_directory(directory_path):
    for root, _, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            clean_file(file_path)

def main(argv=None):
    print("Running clean_paths_files.py")
    parser = argparse.ArgumentParser()
    parser.add_argument('paths', nargs='*', help='Paths to directories or files to clean')
    args = parser.parse_args(argv)

    for path in args.paths:
        if os.path.isdir(path):
            clean_directory(path)
        elif os.path.isfile(path):
            clean_file(path)
        else:
            print(f"Invalid path or file not found: {path}")

    print("Finished running clean_paths_files.py")

if __name__ == '__main__':
    import sys
    sys.exit(main())

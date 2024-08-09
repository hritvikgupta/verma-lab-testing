import re
import os
import argparse
import subprocess

def clean_file(file_path, patterns):
    if file_path.endswith("clean_paths_files.py"):
        return False

    print(f"Cleaning file: {file_path}")
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # Replace each pattern in the content with 'dummy'
        modified = False
        for pattern in patterns:
            replacement = 'dummy'
            cleaned_content = re.sub(re.escape(pattern), replacement, content)
            if content != cleaned_content:
                content = cleaned_content
                modified = True

        if modified:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)
            print(f"File modified: {file_path}")
            return True
        else:
            print(f"No changes needed for file: {file_path}")
            return False

    except Exception as e:
        print(f"Error cleaning file: {e}")
        return False

def clean_staged_files(patterns):
    staged_files = subprocess.check_output(['git', 'diff', '--cached', '--name-only']).decode().splitlines()
    
    modified_files = []
    for file_path in staged_files:
        if os.path.exists(file_path):
            if clean_file(file_path, patterns):
                modified_files.append(file_path)
    
    if modified_files:
        subprocess.check_call(["git", "add"] + modified_files)
        print("Re-staged modified files.")
        print("Please review the changes before committing.")
        return 1  # Return non-zero to abort the commit
    return 0

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('patterns', nargs='+', help='List of patterns to replace with "dummy"')
    args, unknown = parser.parse_known_args()

    return clean_staged_files(args.patterns)

if __name__ == '__main__':
    exit(main())

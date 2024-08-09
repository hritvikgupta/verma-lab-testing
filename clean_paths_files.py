import re
import os
import argparse
import subprocess

def clean_file(file_path, patterns, replacement):
    # Exclude specific files, such as the pre-commit YAML config file
    if file_path.endswith(".yaml") or file_path.endswith(".yml") or file_path.endswith("clean_paths_files.py") or file_path.endswith(".pre-commit-config.yaml"):
        return False

    print(f"Cleaning file: {file_path}")
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        cleaned_content = content
        for pattern in patterns:
            cleaned_content = re.sub(pattern, replacement, cleaned_content)

        if content != cleaned_content:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(cleaned_content)
            print(f"File modified: {file_path}")
            return True
        else:
            print(f"No changes needed for file: {file_path}")
            return False

    except Exception as e:
        print(f"Error cleaning file: {e}")
        return False

def clean_staged_files(patterns, replacement, include_dirs=None):
    staged_files = subprocess.check_output(['git', 'diff', '--cached', '--name-only']).decode().splitlines()
    
    modified_files = []
    for file_path in staged_files:
        # Ensure the file is in one of the included directories
        if include_dirs and not any(file_path.startswith(include_dir) for include_dir in include_dirs):
            continue

        if os.path.exists(file_path):
            if clean_file(file_path, patterns, replacement):
                modified_files.append(file_path)
    
    if modified_files:
        subprocess.check_call(["git", "add"] + modified_files)
        print(f"Re-staged modified files.")
        print("Please review the changes before committing.")
        return 1  # Return non-zero to abort the commit
    return 0

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('patterns', nargs='+', help='Patterns to clean')
    parser.add_argument('--directories', help='Comma-separated list of directories to search', default="")
    parser.add_argument('--replacement', help='Replacement string', default='dummy')
    args, unknown = parser.parse_known_args()

    patterns = [re.escape(pattern) for pattern in args.patterns]
    replacement = args.replacement

    include_dirs = args.directories.split(',') if args.directories else None

    return clean_staged_files(patterns, replacement, include_dirs)

if __name__ == '__main__':
    exit(main())

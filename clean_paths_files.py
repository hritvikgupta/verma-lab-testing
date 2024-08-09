import re
import os
import argparse
import subprocess

def clean_file(file_path, directories):
    if file_path.endswith("clean_paths_files.py"):
        return False

    print(f"Cleaning file: {file_path}")
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        modified = False
        for directory in directories:
            pattern = fr'/{directory}/file_param_name.extension'  # Updated to use each directory argument
            replacement = 'dummy/file_param_name.extension'
            
            # Replace content if pattern is found
            new_content = re.sub(pattern, replacement, content)
            if new_content != content:
                content = new_content
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

def clean_staged_files(directories):
    staged_files = subprocess.check_output(['git', 'diff', '--cached', '--name-only']).decode().splitlines()
    
    modified_files = []
    for file_path in staged_files:
        if any(file_path.startswith(directory) for directory in directories) and os.path.exists(file_path):
            if clean_file(file_path, directories):
                modified_files.append(file_path)
    
    if modified_files:
        subprocess.check_call(["git", "add"] + modified_files)
        print(f"Re-staged modified files.")
        print("Please review the changes before committing.")
        return 1  # Return non-zero to abort the commit
    return 0

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('directories', nargs='+', help='List of directories to clean (e.g., PMBB home)')
    args = parser.parse_args()

    return clean_staged_files(args.directories)

if __name__ == '__main__':
    exit(main())

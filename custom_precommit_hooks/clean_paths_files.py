# import re
# import os
# import argparse
# import subprocess
# #
# def clean_file(file_path, patterns, replacement):
#     # Exclude specific files, such as the pre-commit YAML config file
#     if file_path.endswith(".yaml") or file_path.endswith(".yml") or file_path.endswith("clean_paths_files.py") or file_path.endswith(".pre-commit-config.yaml"):
#         return False

#     print(f"Cleaning file: {file_path}")
#     try:
#         with open(file_path, 'r', encoding='utf-8') as file:
#             content = file.read()

#         cleaned_content = content
#         for pattern in patterns:
#             cleaned_content = re.sub(pattern, replacement, cleaned_content)

#         if content != cleaned_content:
#             with open(file_path, 'w', encoding='utf-8') as file:
#                 file.write(cleaned_content)
#             print(f"File modified: {file_path}")
#             return True
#         else:
#             print(f"No changes needed for file: {file_path}")
#             return False

#     except Exception as e:
#         print(f"Error cleaning file: {e}")
#         return False

# def clean_staged_files(patterns, replacement, include_dirs=None):
#     staged_files = subprocess.check_output(['git', 'diff', '--cached', '--name-only']).decode().splitlines()
    
#     modified_files = []
#     for file_path in staged_files:
#         # Ensure the file is in one of the included directories
#         if include_dirs and not any(file_path.startswith(include_dir) for include_dir in include_dirs):
#             continue

#         if os.path.exists(file_path):
#             if clean_file(file_path, patterns, replacement):
#                 modified_files.append(file_path)
    
#     if modified_files:
#         subprocess.check_call(["git", "add"] + modified_files)
#         print(f"Re-staged modified files.")
#         print("Please review the changes before committing.")
#         return 1  # Return non-zero to abort the commit
#     return 0

# def main():
#     parser = argparse.ArgumentParser()
#     parser.add_argument('patterns', nargs='+', help='Patterns to clean')
#     parser.add_argument('--directories', help='Comma-separated list of directories to search', default="")
#     parser.add_argument('--replacement', help='Replacement string', default='dummy')
#     args, unknown = parser.parse_known_args()

#     patterns = [re.escape(pattern) for pattern in args.patterns]
#     replacement = args.replacement

#     include_dirs = args.directories.split(',') if args.directories else None

#     return clean_staged_files(patterns, replacement, include_dirs)

# if __name__ == '__main__':
#     exit(main())


# import re
# import os
# import argparse
# import subprocess
# import glob

# def clean_file(file_path, patterns, replacement):
#   # Exclude specific files, such as the pre-commit YAML config file
#   if file_path.endswith(".yaml") or file_path.endswith(".yml") or file_path.endswith("clean_paths_files.py") or file_path.endswith(".pre-commit-config.yaml"):
#       return False

#   print(f"Cleaning file: {file_path}")
#   try:
#       with open(file_path, 'r', encoding='utf-8') as file:
#           content = file.read()

#       cleaned_content = content
#       for pattern in patterns:
#           cleaned_content = re.sub(pattern, replacement, cleaned_content)

#       if content != cleaned_content:
#           with open(file_path, 'w', encoding='utf-8') as file:
#               file.write(cleaned_content)
#           print(f"File modified: {file_path}")
#           return True
#       else:
#           print(f"No changes needed for file: {file_path}")
#           return False

#   except Exception as e:
#       print(f"Error cleaning file: {e}")
#       return False

# def clean_staged_files(patterns, replacement, include_dirs=None):
#   staged_files = subprocess.check_output(['git', 'diff', '--cached', '--name-only']).decode().splitlines()
  
#   modified_files = []
#   for file_path in staged_files:
#       # Check if the file is in one of the included directories or their subdirectories
#       if include_dirs:
#           if not any(file_path.startswith(os.path.normpath(include_dir)) for include_dir in include_dirs):
#               continue
      
#       if os.path.exists(file_path):
#           if clean_file(file_path, patterns, replacement):
#               modified_files.append(file_path)
  
#   if modified_files:
#       subprocess.check_call(["git", "add"] + modified_files)
#       print(f"Re-staged modified files.")
#       print("Please review the changes before committing.")
#       return 1  # Return non-zero to abort the commit
#   return 0

# def main():
#   parser = argparse.ArgumentParser()
#   parser.add_argument('patterns', nargs='+', help='Patterns to clean')
#   parser.add_argument('--directories', help='Comma-separated list of directories to search', default="")
#   parser.add_argument('--replacement', help='Replacement string', default='dummy')
#   args, unknown = parser.parse_known_args()

#   patterns = [re.escape(pattern) for pattern in args.patterns]
#   replacement = args.replacement

#   include_dirs = args.directories.split(',') if args.directories else None
  
#   # Expand directory names to include all matching directories
#   if include_dirs:
#       expanded_dirs = []
#       for dir_pattern in include_dirs:
#           matching_dirs = glob.glob(dir_pattern)
#           expanded_dirs.extend(matching_dirs)
#       include_dirs = expanded_dirs

#   return clean_staged_files(patterns, replacement, include_dirs)

# if __name__ == '__main__':
#   exit(main())

# import re
# import os
# import argparse
# import subprocess
# import glob

# def clean_file(file_path, patterns, replacement):
#   # Exclude specific files, such as the pre-commit YAML config file
#   if file_path.endswith(".yaml") or file_path.endswith(".yml") or file_path.endswith("clean_paths_files.py") or file_path.endswith(".pre-commit-config.yaml"):
#       return False

#   print(f"Cleaning file: {file_path}")
#   try:
#       with open(file_path, 'r', encoding='utf-8') as file:
#           content = file.read()

#       cleaned_content = content
#       for pattern in patterns:
#           # Create a more flexible regex pattern
#           flexible_pattern = re.compile(rf'(?i)(?:^|[/\\])(?:{re.escape(pattern)}(?:_\w+)?)(?:/|\\|$).*?(?=[\'"\s]|$)')

#           def replace_path(match):
#               full_path = match.group(0)
#               filename = os.path.basename(full_path.rstrip('/\\'))
#               return os.path.join(replacement, filename)

#           cleaned_content = flexible_pattern.sub(replace_path, cleaned_content)

#       if content != cleaned_content:
#           with open(file_path, 'w', encoding='utf-8') as file:
#               file.write(cleaned_content)
#           print(f"File modified: {file_path}")
#           return True
#       else:
#           print(f"No changes needed for file: {file_path}")
#           return False

#   except Exception as e:
#       print(f"Error cleaning file: {e}")
#       return False


# def clean_staged_files(patterns, replacement, include_dirs=None):
#   staged_files = subprocess.check_output(['git', 'diff', '--cached', '--name-only']).decode().splitlines()
  
#   modified_files = []
#   for file_path in staged_files:
#       # Check if the file is in one of the included directories or their subdirectories
#       if include_dirs:
#           if not any(file_path.startswith(os.path.normpath(include_dir)) for include_dir in include_dirs):
#               continue
      
#       if os.path.exists(file_path):
#           if clean_file(file_path, patterns, replacement):
#               modified_files.append(file_path)
  
#   if modified_files:
#       subprocess.check_call(["git", "add"] + modified_files)
#       print(f"Re-staged modified files.")
#       print("Please review the changes before committing.")
#       return 1  # Return non-zero to abort the commit
#   return 0

# def main():
#   parser = argparse.ArgumentParser()
#   parser.add_argument('patterns', nargs='+', help='Patterns to clean')
#   parser.add_argument('--directories', help='Comma-separated list of directories to search', default="")
#   parser.add_argument('--replacement', help='Replacement string', default='dummy')
#   args, unknown = parser.parse_known_args()

#   patterns = [re.escape(pattern) for pattern in args.patterns]
#   replacement = args.replacement

#   include_dirs = args.directories.split(',') if args.directories else None
  
#   # Expand directory names to include all matching directories
#   if include_dirs:
#       expanded_dirs = []
#       for dir_pattern in include_dirs:
#           matching_dirs = glob.glob(dir_pattern)
#           expanded_dirs.extend(matching_dirs)
#       include_dirs = expanded_dirs

#   return clean_staged_files(patterns, replacement, include_dirs)

# if __name__ == '__main__':
#   exit(main())


# import re
# import os
# import argparse
# import subprocess
# import glob
# import logging

# def clean_file(file_path, patterns, replacement):
#     # Exclude specific files, such as the pre-commit YAML config file
#     if file_path.endswith(".yaml") or file_path.endswith(".yml") or file_path.endswith("clean_paths_files.py") or file_path.endswith(".pre-commit-config.yaml"):
#         return False

#     print(f"Cleaning file: {file_path}")
#     try:
#         with open(file_path, 'r', encoding='utf-8') as file:
#             content = file.read()

#         cleaned_content = content
#         for pattern in patterns:
#             # Create a more flexible regex pattern
#             flexible_pattern = re.compile(rf'(?i)(?:^|[/\\])(?:{re.escape(pattern)}(?:_\w+)?)(?:/|\\|$).*?(?=[\'"\s]|$)')

#             def replace_path(match):
#                 full_path = match.group(0)
#                 filename = os.path.basename(full_path.rstrip('/\\'))
#                 return os.path.join(replacement, filename)

#             cleaned_content = flexible_pattern.sub(replace_path, cleaned_content)

#         if content != cleaned_content:
#             with open(file_path, 'w', encoding='utf-8') as file:
#                 file.write(cleaned_content)
#             print(f"File modified: {file_path}")
#             return True
#         else:
#             print(f"No changes needed for file: {file_path}")
#             return False

#     except Exception as e:
#         print(f"Error cleaning file: {e}")
#         return False


# def clean_files(patterns, replacement, include_dirs=None, enforce_all=False):
#     if enforce_all:
#         # Find all relevant files in the repository
#         all_files = []
#         for root, _, files in os.walk('.'):
#             for file in files:
#                 file_path = os.path.join(root, file)
#                 if include_dirs:
#                     if any(os.path.abspath(file_path).startswith(os.path.abspath(include_dir)) for include_dir in include_dirs):
#                         all_files.append(file_path)
#                 else:
#                     all_files.append(file_path)
#         relevant_files = all_files
#     else:
#         # Find staged files
#         relevant_files = subprocess.check_output(['git', 'diff', '--cached', '--name-only']).decode().splitlines()

#     modified_files = []
#     for file_path in relevant_files:
#         if os.path.exists(file_path):
#             if clean_file(file_path, patterns, replacement):
#                 modified_files.append(file_path)
    
#     if modified_files:
#         subprocess.check_call(["git", "add"] + modified_files)
#         print(f"Re-staged modified files.")
#         print("Please review the changes before committing.")
#         return 1  # Return non-zero to abort the commit
#     return 0

# def main():
#     logging.info("\n### Cleaning Files Hook ###")
#     parser = argparse.ArgumentParser()
#     parser.add_argument('patterns', nargs='+', help='Patterns to clean')
#     parser.add_argument('--directories', help='Comma-separated list of directories to search', default="")
#     parser.add_argument('--replacement', help='Replacement string', default='dummy')
#     parser.add_argument('--enforce-all', action='store_true', help='Enforce cleaning all relevant files, not just staged files')
#     args, unknown = parser.parse_known_args()

#     patterns = [re.escape(pattern) for pattern in args.patterns]
#     replacement = args.replacement

#     include_dirs = args.directories.split(',') if args.directories else None
    
#     # Expand directory names to include all matching directories
#     if include_dirs:
#         expanded_dirs = []
#         for dir_pattern in include_dirs:
#             matching_dirs = glob.glob(dir_pattern)
#             expanded_dirs.extend(matching_dirs)
#         include_dirs = expanded_dirs

#     return clean_files(patterns, replacement, include_dirs, args.enforce_all)

# if __name__ == '__main__':
#     # exit(main())
#     logging.basicConfig(filename='pre_commit.log', level=logging.INFO)
#     raise SystemExit(main())

import re
import os
import argparse
import subprocess
import glob
import logging
import json

def clean_file(file_path, patterns, replacement):
    if is_binary_file(file_path):
        logging.info(f"Skipping binary file: {file_path}")
        return False
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        logging.info(f"Original content of {file_path}:\n{content[:200]}")  # Show first 200 characters for brevity

        cleaned_content = content
        for pattern in patterns:
            flexible_pattern = re.compile(rf'(?i)(?:^|[/\\])(?:{re.escape(pattern)}(?:_\w+)?)(?:/|\\|$).*?(?=[\'"\s]|$)')
            matches = flexible_pattern.findall(content)
            if matches:
                logging.info(f"Pattern '{pattern}' found in {file_path}: {matches}")
            else:
                logging.info(f"Pattern '{pattern}' not found in {file_path}")

            def replace_path(match):
                full_path = match.group(0)
                filename = os.path.basename(full_path.rstrip('/\\'))
                return os.path.join(replacement, filename)

            cleaned_content = flexible_pattern.sub(replace_path, cleaned_content)

        if content != cleaned_content:
            logging.info(f"Modified content of {file_path}:\n{cleaned_content[:200]}")  # Show first 200 characters for brevity
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(cleaned_content)
            logging.info(f"File modified: {file_path}")
            return True
        else:
            logging.info(f"No changes needed for file: {file_path}")
            return False

    except Exception as e:
        logging.error(f"Error cleaning file {file_path}: {e}")
        return False


def clean_files(patterns, replacement, include_dirs=None, enforce_all=False):
    if enforce_all:
        all_files = []
        for root, _, files in os.walk('.'):
            for file in files:
                file_path = os.path.join(root, file)
                if include_dirs:
                    if any(os.path.abspath(file_path).startswith(os.path.abspath(include_dir)) for include_dir in include_dirs):
                        all_files.append(file_path)
                else:
                    all_files.append(file_path)
        relevant_files = all_files
    else:
        relevant_files = subprocess.check_output(['git', 'diff', '--cached', '--name-only']).decode().splitlines()

    modified_files = []
    for file_path in relevant_files:
        if os.path.exists(file_path):
            if clean_file(file_path, patterns, replacement):
                modified_files.append(file_path)
    
    if modified_files:
        subprocess.check_call(["git", "add"] + modified_files)
        logging.info(f"Re-staged modified files.")
        logging.info("Please review the changes before committing.")
        return 1  # Return non-zero to abort the commit
    return 0

def main():
    logging.info("\n### Cleaning Files Hook ###")
    parser = argparse.ArgumentParser()
    parser.add_argument('patterns', nargs='*', help='Patterns to clean')
    parser.add_argument('--directories', help='Comma-separated list of directories to search', default="")
    parser.add_argument('--replacement', help='Replacement string', default='dummy')
    parser.add_argument('--json-config', help='Path to JSON config file', type=str)
    parser.add_argument('--enforce-all', action='store_true', help='Enforce cleaning all relevant files, not just staged files')
    args, unknown = parser.parse_known_args()

    if args.json_config:
        with open(args.json_config, 'r') as f:
            config = json.load(f)
            patterns = [re.escape(pattern) for pattern in config['patterns']]
            replacement = config['replacement']
            include_dirs = config['directories']
            logging.info(f"Loaded JSON config: {config}")
    else:
        patterns = [re.escape(pattern) for pattern in args.patterns]
        replacement = args.replacement
        include_dirs = args.directories.split(',') if args.directories else None

    if include_dirs:
        expanded_dirs = []
        for dir_pattern in include_dirs:
            matching_dirs = glob.glob(dir_pattern)
            expanded_dirs.extend(matching_dirs)
        include_dirs = expanded_dirs

    return clean_files(patterns, replacement, include_dirs, args.enforce_all)

if __name__ == '__main__':
    logging.basicConfig(filename='pre_commit.log', level=logging.INFO)
    raise SystemExit(main())



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

# import re
# import os
# import argparse
# import subprocess
# import glob
# import logging
# import json

# def is_binary_file(filepath):
#     try:
#         with open(filepath, 'rb') as file:
#             for block in iter(lambda: file.read(1024), b''):
#                 if b'\0' in block:
#                     return True
#         return False
#     except Exception as e:
#         logging.error(f"Error checking if file is binary: {e}")
#         return False  # Assume non-binary on error

# def clean_file(filepath, patterns, replacement):
#     if is_binary_file(filepath):
#         logging.info(f"Skipping binary file: {filepath}")
#         return False
    
#     try:
#         with open(filepath, 'r', encoding='utf-8') as file:
#             content = file.read()

#         logging.info(f"Original content of {filepath}:\n{content[:200]}")  # Show first 200 characters for brevity

#         cleaned_content = content
#         for pattern in patterns:
#             # Adjusted regex for more specific matching
#             flexible_pattern = re.compile(
#                 rf'(?i)(?:{re.escape(pattern)}(?:_\w+)?)(?=\s*=)',
#                 re.MULTILINE
#             )
#             matches = flexible_pattern.findall(content)
#             if matches:
#                 logging.info(f"Pattern '{pattern}' found in {filepath}: {matches}")
#             else:
#                 logging.info(f"Pattern '{pattern}' not found in {filepath}")

#             def replace_path(match):
#                 full_path = match.group(0)
#                 logging.info(f"Replacing path: {full_path} with {replacement}")
#                 return replacement

#             cleaned_content = flexible_pattern.sub(replace_path, cleaned_content)

#         if content != cleaned_content:
#             logging.info(f"Modified content of {filepath}:\n{cleaned_content[:200]}")  # Show first 200 characters for brevity
#             with open(filepath, 'w', encoding='utf-8') as file:
#                 file.write(cleaned_content)
#             logging.info(f"File modified: {filepath}")
#             return True
#         else:
#             logging.info(f"No changes needed for file: {filepath}")
#             return False

#     except Exception as e:
#         logging.error(f"Error cleaning file {filepath}: {e}")
#         return False


# def clean_files(patterns, replacement, include_dirs=None, enforce_all=False):
#     if enforce_all:
#         all_files = []
#         for root, _, files in os.walk('.'):
#             for file in files:
#                 filepath = os.path.join(root, file)
#                 if include_dirs:
#                     if any(os.path.abspath(filepath).startswith(os.path.abspath(include_dir)) for include_dir in include_dirs):
#                         all_files.append(filepath)
#                 else:
#                     all_files.append(filepath)
#         relevant_files = all_files
#     else:
#         relevant_files = subprocess.check_output(['git', 'diff', '--cached', '--name-only']).decode().splitlines()

#     modified_files = []
#     for filepath in relevant_files:
#         if os.path.exists(filepath):
#             if clean_file(filepath, patterns, replacement):
#                 modified_files.append(filepath)
    
#     if modified_files:
#         subprocess.check_call(["git", "add"] + modified_files)
#         logging.info(f"Re-staged modified files.")
#         logging.info("Please review the changes before committing.")
#         return 1  # Return non-zero to abort the commit
#     return 0

# def main():
#     logging.info("\n### Cleaning Files Hook ###")
#     parser = argparse.ArgumentParser()
#     parser.add_argument('patterns', nargs='*', help='Patterns to clean')
#     parser.add_argument('--directories', help='Comma-separated list of directories to search', default="")
#     parser.add_argument('--replacement', help='Replacement string', default='dummy')
#     parser.add_argument('--json-config', help='Path to JSON config file', type=str)
#     parser.add_argument('--enforce-all', action='store_true', help='Enforce cleaning all relevant files, not just staged files')
#     args, unknown = parser.parse_known_args()

#     if args.json_config:
#         with open(args.json_config, 'r') as f:
#             config = json.load(f)
#             patterns = [re.escape(pattern) for pattern in config['patterns']]
#             replacement = config['replacement']
#             include_dirs = config['directories']
#             logging.info(f"Loaded JSON config: {config}")
#     else:
#         patterns = [re.escape(pattern) for pattern in args.patterns]
#         replacement = args.replacement
#         include_dirs = args.directories.split(',') if args.directories else None

#     if include_dirs:
#         expanded_dirs = []
#         for dir_pattern in include_dirs:
#             matching_dirs = glob.glob(dir_pattern)
#             expanded_dirs.extend(matching_dirs)
#         include_dirs = expanded_dirs

#     return clean_files(patterns, replacement, include_dirs, args.enforce_all)

# if __name__ == '__main__':
#     logging.basicConfig(filename='pre_commit.log', level=logging.INFO)
#     raise SystemExit(main())


# import re
# import os
# import argparse
# import subprocess
# import glob
# import logging
# import json

# def is_binary_file(filepath):
#     try:
#         with open(filepath, 'rb') as file:
#             for block in iter(lambda: file.read(1024), b''):
#                 if b'\0' in block:
#                     return True
#         return False
#     except Exception as e:
#         logging.error(f"Error checking if file is binary: {e}")
#         return False  # Assume non-binary on error

# def clean_file(filepath, patterns, replacement):
#     if is_binary_file(filepath):
#         logging.info(f"Skipping binary file: {filepath}")
#         return False
    
#     try:
#         with open(filepath, 'r', encoding='utf-8') as file:
#             content = file.read()

#         logging.info(f"Original content of {filepath}:\n{content[:200]}")  # Show first 200 characters for brevity

#         cleaned_content = content
#         for pattern in patterns:
#             # Adjusted regex to capture the value after '='
#             flexible_pattern = re.compile(
#                 rf'(?P<key>{re.escape(pattern)})(\s*=\s*)(?P<value>[^\n]*)',
#                 re.MULTILINE
#             )
#             matches = flexible_pattern.findall(content)
#             if matches:
#                 logging.info(f"Pattern '{pattern}' found in {filepath}: {matches}")
#             else:
#                 logging.info(f"Pattern '{pattern}' not found in {filepath}")

#             def replace_value(match):
#                 key = match.group('key')
#                 value = match.group('value')
#                 logging.info(f"Replacing value for key '{key}': {value} with {replacement}")
#                 return f"{key} = {replacement}"

#             cleaned_content = flexible_pattern.sub(replace_value, cleaned_content)

#         if content != cleaned_content:
#             logging.info(f"Modified content of {filepath}:\n{cleaned_content[:200]}")  # Show first 200 characters for brevity
#             with open(filepath, 'w', encoding='utf-8') as file:
#                 file.write(cleaned_content)
#             logging.info(f"File modified: {filepath}")
#             return True
#         else:
#             logging.info(f"No changes needed for file: {filepath}")
#             return False

#     except Exception as e:
#         logging.error(f"Error cleaning file {filepath}: {e}")
#         return False


# def clean_files(patterns, replacement, include_dirs=None, enforce_all=False):
#     if enforce_all:
#         all_files = []
#         for root, _, files in os.walk('.'):
#             for file in files:
#                 filepath = os.path.join(root, file)
#                 if include_dirs:
#                     if any(os.path.abspath(filepath).startswith(os.path.abspath(include_dir)) for include_dir in include_dirs):
#                         all_files.append(filepath)
#                 else:
#                     all_files.append(filepath)
#         relevant_files = all_files
#     else:
#         relevant_files = subprocess.check_output(['git', 'diff', '--cached', '--name-only']).decode().splitlines()

#     modified_files = []
#     for filepath in relevant_files:
#         if os.path.exists(filepath):
#             if clean_file(filepath, patterns, replacement):
#                 modified_files.append(filepath)
    
#     if modified_files:
#         subprocess.check_call(["git", "add"] + modified_files)
#         logging.info(f"Re-staged modified files.")
#         logging.info("Please review the changes before committing.")
#         return 1  # Return non-zero to abort the commit
#     return 0

# def main():
#     logging.info("\n### Cleaning Files Hook ###")
#     parser = argparse.ArgumentParser()
#     parser.add_argument('patterns', nargs='*', help='Patterns to clean')
#     parser.add_argument('--directories', help='Comma-separated list of directories to search', default="")
#     parser.add_argument('--replacement', help='Replacement string', default='dummy')
#     parser.add_argument('--json-config', help='Path to JSON config file', type=str)
#     parser.add_argument('--enforce-all', action='store_true', help='Enforce cleaning all relevant files, not just staged files')
#     args, unknown = parser.parse_known_args()

#     if args.json_config:
#         with open(args.json_config, 'r') as f:
#             config = json.load(f)
#             patterns = [re.escape(pattern) for pattern in config['patterns']]
#             replacement = config['replacement']
#             include_dirs = config['directories']
#             logging.info(f"Loaded JSON config: {config}")
#     else:
#         patterns = [re.escape(pattern) for pattern in args.patterns]
#         replacement = args.replacement
#         include_dirs = args.directories.split(',') if args.directories else None

#     if include_dirs:
#         expanded_dirs = []
#         for dir_pattern in include_dirs:
#             matching_dirs = glob.glob(dir_pattern)
#             expanded_dirs.extend(matching_dirs)
#         include_dirs = expanded_dirs

#     return clean_files(patterns, replacement, include_dirs, args.enforce_all)

# if __name__ == '__main__':
#     logging.basicConfig(filename='pre_commit.log', level=logging.INFO)
#     raise SystemExit(main())

# import re
# import os
# import argparse
# import subprocess
# import glob
# import logging
# import json

# def is_binary_file(filepath):
#     try:
#         with open(filepath, 'rb') as file:
#             for block in iter(lambda: file.read(1024), b''):
#                 if b'\0' in block:
#                     return True
#         return False
#     except Exception as e:
#         logging.error(f"Error checking if file is binary: {e}")
#         return False  # Assume non-binary on error

# def clean_file(filepath, patterns, replacement):
#     if is_binary_file(filepath):
#         logging.info(f"Skipping binary file: {filepath}")
#         return False
    
#     try:
#         with open(filepath, 'r', encoding='utf-8') as file:
#             content = file.read()

#         logging.info(f"Original content of {filepath}:\n{content[:200]}")  # Show first 200 characters for brevity

#         cleaned_content = content
#         for pattern in patterns:
#             # Adjusted regex to capture the value after '='
#             flexible_pattern = re.compile(
#                 rf'(?P<key>{pattern})(\s*=\s*)(?P<value>[^\n]*)',
#                 re.MULTILINE
#             )
#             matches = flexible_pattern.findall(content)
#             if matches:
#                 logging.info(f"Pattern '{pattern}' found in {filepath}: {matches}")
#             else:
#                 logging.info(f"Pattern '{pattern}' not found in {filepath}")

#             def replace_value(match):
#                 key = match.group('key')
#                 value = match.group('value')
#                 logging.info(f"Replacing value for key '{key}': {value} with {replacement}")
#                 return f"{key} = {replacement}"

#             cleaned_content = flexible_pattern.sub(replace_value, cleaned_content)

#         if content != cleaned_content:
#             logging.info(f"Modified content of {filepath}:\n{cleaned_content[:200]}")  # Show first 200 characters for brevity
#             with open(filepath, 'w', encoding='utf-8') as file:
#                 file.write(cleaned_content)
#             logging.info(f"File modified: {filepath}")
#             return True
#         else:
#             logging.info(f"No changes needed for file: {filepath}")
#             return False

#     except Exception as e:
#         logging.error(f"Error cleaning file {filepath}: {e}")
#         return False


# def clean_files(patterns, replacement, include_dirs=None, enforce_all=False):
#     if enforce_all:
#         all_files = []
#         for root, _, files in os.walk('.'):
#             for file in files:
#                 filepath = os.path.join(root, file)
#                 if include_dirs:
#                     if any(os.path.abspath(filepath).startswith(os.path.abspath(include_dir)) for include_dir in include_dirs):
#                         all_files.append(filepath)
#                 else:
#                     all_files.append(filepath)
#         relevant_files = all_files
#     else:
#         relevant_files = subprocess.check_output(['git', 'diff', '--cached', '--name-only']).decode().splitlines()

#     modified_files = []
#     for filepath in relevant_files:
#         if os.path.exists(filepath):
#             if clean_file(filepath, patterns, replacement):
#                 modified_files.append(filepath)
    
#     if modified_files:
#         subprocess.check_call(["git", "add"] + modified_files)
#         logging.info(f"Re-staged modified files.")
#         logging.info("Please review the changes before committing.")
#         return 1  # Return non-zero to abort the commit
#     return 0

# def main():
#     logging.info("\n### Cleaning Files Hook ###")
#     parser = argparse.ArgumentParser()
#     parser.add_argument('patterns', nargs='*', help='Patterns to clean')
#     parser.add_argument('--directories', help='Comma-separated list of directories to search', default="")
#     parser.add_argument('--replacement', help='Replacement string', default='dummy')
#     parser.add_argument('--json-config', help='Path to JSON config file', type=str)
#     parser.add_argument('--enforce-all', action='store_true', help='Enforce cleaning all relevant files, not just staged files')
#     args, unknown = parser.parse_known_args()

#     if args.json_config:
#         with open(args.json_config, 'r') as f:
#             config = json.load(f)
#             patterns = config['patterns']  # No re.escape needed
#             replacement = config['replacement']
#             include_dirs = config['directories']
#             logging.info(f"Loaded JSON config: {config}")
#     else:
#         patterns = args.patterns  # No re.escape needed
#         replacement = args.replacement
#         include_dirs = args.directories.split(',') if args.directories else None

#     if include_dirs:
#         expanded_dirs = []
#         for dir_pattern in include_dirs:
#             matching_dirs = glob.glob(dir_pattern)
#             expanded_dirs.extend(matching_dirs)
#         include_dirs = expanded_dirs

#     return clean_files(patterns, replacement, include_dirs, args.enforce_all)

# if __name__ == '__main__':
#     logging.basicConfig(filename='pre_commit.log', level=logging.INFO)
#     raise SystemExit(main())



# import re
# import os
# import argparse
# import subprocess
# import glob
# import logging
# import json

# def is_binary_file(filepath):
#     try:
#         with open(filepath, 'rb') as file:
#             for block in iter(lambda: file.read(1024), b''):
#                 if b'\0' in block:
#                     return True
#         return False
#     except Exception as e:
#         logging.error(f"Error checking if file is binary: {e}")
#         return False  # Assume non-binary on error

# def clean_file(filepath, patterns):
#     if is_binary_file(filepath):
#         logging.info(f"Skipping binary file: {filepath}")
#         return False
    
#     try:
#         with open(filepath, 'r', encoding='utf-8') as file:
#             content = file.read()

#         logging.info(f"Original content of {filepath}:\n{content[:200]}")  # Show first 200 characters for brevity

#         cleaned_content = content
#         for pattern, replacement in patterns.items():
#             # Adjusted regex to capture the value after '='
#             flexible_pattern = re.compile(
#                 rf'(?P<key>{pattern})(\s*=\s*)(?P<value>[^\n]*)',
#                 re.MULTILINE
#             )
#             matches = flexible_pattern.findall(content)
#             if matches:
#                 logging.info(f"Pattern '{pattern}' found in {filepath}: {matches}")
#             else:
#                 logging.info(f"Pattern '{pattern}' not found in {filepath}")

#             def replace_value(match):
#                 key = match.group('key')
#                 value = match.group('value')
#                 logging.info(f"Replacing value for key '{key}': {value} with {replacement}")
#                 return f"{key} = {replacement}"

#             cleaned_content = flexible_pattern.sub(replace_value, cleaned_content)

#         if content != cleaned_content:
#             logging.info(f"Modified content of {filepath}:\n{cleaned_content[:200]}")  # Show first 200 characters for brevity
#             with open(filepath, 'w', encoding='utf-8') as file:
#                 file.write(cleaned_content)
#             logging.info(f"File modified: {filepath}")
#             return True
#         else:
#             logging.info(f"No changes needed for file: {filepath}")
#             return False

#     except Exception as e:
#         logging.error(f"Error cleaning file {filepath}: {e}")
#         return False


# def clean_files(patterns, include_dirs=None, enforce_all=False):
#     if enforce_all:
#         all_files = []
#         for root, _, files in os.walk('.'):
#             for file in files:
#                 filepath = os.path.join(root, file)
#                 if include_dirs:
#                     if any(os.path.abspath(filepath).startswith(os.path.abspath(include_dir)) for include_dir in include_dirs):
#                         all_files.append(filepath)
#                 else:
#                     all_files.append(filepath)
#         relevant_files = all_files
#     else:
#         relevant_files = subprocess.check_output(['git', 'diff', '--cached', '--name-only']).decode().splitlines()

#     modified_files = []
#     for filepath in relevant_files:
#         if os.path.exists(filepath):
#             if clean_file(filepath, patterns):
#                 modified_files.append(filepath)
    
#     if modified_files:
#         subprocess.check_call(["git", "add"] + modified_files)
#         logging.info(f"Re-staged modified files.")
#         logging.info("Please review the changes before committing.")
#         return 1  # Return non-zero to abort the commit
#     return 0

# def main():
#     logging.info("\n### Cleaning Files Hook ###")
#     parser = argparse.ArgumentParser()
#     parser.add_argument('--json-config', help='Path to JSON config file', type=str)
#     parser.add_argument('--enforce-all', action='store_true', help='Enforce cleaning all relevant files, not just staged files')
#     args, unknown = parser.parse_known_args()

#     if args.json_config:
#         with open(args.json_config, 'r') as f:
#             config = json.load(f)
#             patterns = config['patterns']
#             include_dirs = config['directories']
#             logging.info(f"Loaded JSON config: {config}")
#     else:
#         logging.error("JSON config file is required.")
#         return 1

#     if include_dirs:
#         expanded_dirs = []
#         for dir_pattern in include_dirs:
#             matching_dirs = glob.glob(dir_pattern)
#             expanded_dirs.extend(matching_dirs)
#         include_dirs = expanded_dirs

#     return clean_files(patterns, include_dirs, args.enforce_all)

# if __name__ == '__main__':
#     logging.basicConfig(filename='pre_commit.log', level=logging.INFO)
#     raise SystemExit(main())

# import re
# import os
# import argparse
# import subprocess
# import glob
# import logging
# import json

# def is_binary_file(filepath):
#     try:
#         with open(filepath, 'rb') as file:
#             for block in iter(lambda: file.read(1024), b''):
#                 if b'\0' in block:
#                     return True
#         return False
#     except Exception as e:
#         logging.error(f"Error checking if file is binary: {e}")
#         return False  # Assume non-binary on error

# def clean_file(filepath, patterns):
#     if is_binary_file(filepath):
#         logging.info(f"Skipping binary file: {filepath}")
#         return False
    
#     try:
#         with open(filepath, 'r', encoding='utf-8') as file:
#             content = file.read()

#         logging.info(f"Original content of {filepath}:\n{content[:200]}")  # Show first 200 characters for brevity

#         cleaned_content = content
#         for pattern, options in patterns.items():
#             replacement = options["replacement"]
#             inplace = options.get("inplace", False)
            
#             if inplace:
#                 flexible_pattern = re.compile(
#                     rf'\b{re.escape(pattern)}\b',
#                     re.MULTILINE
#                 )
#             else:
#                 flexible_pattern = re.compile(
#                     rf'(?P<key>{pattern})(\s*=\s*)(?P<value>[^\n]*)',
#                     re.MULTILINE
#                 )

#             matches = flexible_pattern.findall(content)
#             if matches:
#                 logging.info(f"Pattern '{pattern}' found in {filepath}: {matches}")
#             else:
#                 logging.info(f"Pattern '{pattern}' not found in {filepath}")

#             def replace_value(match):
#                 if inplace:
#                     logging.info(f"Replacing in-place '{match.group(0)}' with '{replacement}'")
#                     return replacement
#                 else:
#                     key = match.group('key')
#                     logging.info(f"Replacing value for key '{key}' with '{replacement}'")
#                     return f"{key} = {replacement}"

#             cleaned_content = flexible_pattern.sub(replace_value, cleaned_content)

#         if content != cleaned_content:
#             logging.info(f"Modified content of {filepath}:\n{cleaned_content[:200]}")  # Show first 200 characters for brevity
#             with open(filepath, 'w', encoding='utf-8') as file:
#                 file.write(cleaned_content)
#             logging.info(f"File modified: {filepath}")
#             return True
#         else:
#             logging.info(f"No changes needed for file: {filepath}")
#             return False

#     except Exception as e:
#         logging.error(f"Error cleaning file {filepath}: {e}")
#         return False


# def clean_files(patterns, include_dirs=None, enforce_all=False):
#     if enforce_all:
#         all_files = []
#         for root, _, files in os.walk('.'):
#             for file in files:
#                 filepath = os.path.join(root, file)
#                 if include_dirs:
#                     if any(os.path.abspath(filepath).startswith(os.path.abspath(include_dir)) for include_dir in include_dirs):
#                         all_files.append(filepath)
#                 else:
#                     all_files.append(filepath)
#         relevant_files = all_files
#     else:
#         relevant_files = subprocess.check_output(['git', 'diff', '--cached', '--name-only']).decode().splitlines()

#     modified_files = []
#     for filepath in relevant_files:
#         if os.path.exists(filepath):
#             if clean_file(filepath, patterns):
#                 modified_files.append(filepath)
    
#     if modified_files:
#         subprocess.check_call(["git", "add"] + modified_files)
#         logging.info(f"Re-staged modified files.")
#         logging.info("Please review the changes before committing.")
#         return 1  # Return non-zero to abort the commit
#     return 0

# def main():
#     logging.info("\n### Cleaning Files Hook ###")
#     parser = argparse.ArgumentParser()
#     parser.add_argument('--json-config', help='Path to JSON config file', type=str)
#     parser.add_argument('--enforce-all', action='store_true', help='Enforce cleaning all relevant files, not just staged files')
#     args, unknown = parser.parse_known_args()

#     if args.json_config:
#         with open(args.json_config, 'r') as f:
#             config = json.load(f)
#             patterns = config['patterns']
#             include_dirs = config['directories']
#             logging.info(f"Loaded JSON config: {config}")
#     else:
#         logging.error("JSON config file is required.")
#         return 1

#     if include_dirs:
#         expanded_dirs = []
#         for dir_pattern in include_dirs:
#             matching_dirs = glob.glob(dir_pattern)
#             expanded_dirs.extend(matching_dirs)
#         include_dirs = expanded_dirs

#     return clean_files(patterns, include_dirs, args.enforce_all)

# if __name__ == '__main__':
#     logging.basicConfig(filename='pre_commit.log', level=logging.INFO)
#     raise SystemExit(main())

# import re
# import os
# import argparse
# import subprocess
# import glob
# import logging
# import json

# def is_binary_file(filepath):
#     try:
#         with open(filepath, 'rb') as file:
#             for block in iter(lambda: file.read(1024), b''):
#                 if b'\0' in block:
#                     return True
#         return False
#     except Exception as e:
#         logging.error(f"Error checking if file is binary: {e}")
#         return False  # Assume non-binary on error

# def should_skip_file(filepath):
#     # Skip JSON and YAML configuration files
#     if filepath.endswith('config.json') or filepath.endswith('.yaml') or filepath.endswith('.yml'):
#         logging.info(f"Skipping configuration file: {filepath}")
#         return True
#     return False

# def clean_file(filepath, patterns):
#     if is_binary_file(filepath):
#         logging.info(f"Skipping binary file: {filepath}")
#         return False

#     if should_skip_file(filepath):
#         return False
    
#     try:
#         with open(filepath, 'r', encoding='utf-8') as file:
#             content = file.read()

#         logging.info(f"Original content of {filepath}:\n{content[:200]}")  # Show first 200 characters for brevity

#         cleaned_content = content
#         for pattern, options in patterns.items():
#             replacement = options["replacement"]
#             inplace = options.get("inplace", False)
            
#             if inplace:
#                 flexible_pattern = re.compile(
#                     rf'\b{re.escape(pattern)}\b',
#                     re.MULTILINE
#                 )
#             else:
#                 flexible_pattern = re.compile(
#                     rf'(?P<key>{pattern})(\s*=\s*)(?P<value>[^\n]*)',
#                     re.MULTILINE
#                 )

#             matches = flexible_pattern.findall(content)
#             if matches:
#                 logging.info(f"Pattern '{pattern}' found in {filepath}: {matches}")
#             else:
#                 logging.info(f"Pattern '{pattern}' not found in {filepath}")

#             def replace_value(match):
#                 if inplace:
#                     logging.info(f"Replacing in-place '{match.group(0)}' with '{replacement}'")
#                     return replacement
#                 else:
#                     key = match.group('key')
#                     logging.info(f"Replacing value for key '{key}' with '{replacement}'")
#                     return f"{key} = {replacement}"

#             cleaned_content = flexible_pattern.sub(replace_value, cleaned_content)

#         if content != cleaned_content:
#             logging.info(f"Modified content of {filepath}:\n{cleaned_content[:200]}")  # Show first 200 characters for brevity
#             with open(filepath, 'w', encoding='utf-8') as file:
#                 file.write(cleaned_content)
#             logging.info(f"File modified: {filepath}")
#             return True
#         else:
#             logging.info(f"No changes needed for file: {filepath}")
#             return False

#     except Exception as e:
#         logging.error(f"Error cleaning file {filepath}: {e}")
#         return False


# def clean_files(patterns, include_dirs=None, enforce_all=False):
#     if enforce_all:
#         all_files = []
#         for root, _, files in os.walk('.'):
#             for file in files:
#                 filepath = os.path.join(root, file)
#                 if include_dirs:
#                     if any(os.path.abspath(filepath).startswith(os.path.abspath(include_dir)) for include_dir in include_dirs):
#                         all_files.append(filepath)
#                 else:
#                     all_files.append(filepath)
#         relevant_files = all_files
#     else:
#         relevant_files = subprocess.check_output(['git', 'diff', '--cached', '--name-only']).decode().splitlines()

#     modified_files = []
#     for filepath in relevant_files:
#         if os.path.exists(filepath):
#             if clean_file(filepath, patterns):
#                 modified_files.append(filepath)
    
#     if modified_files:
#         subprocess.check_call(["git", "add"] + modified_files)
#         logging.info(f"Re-staged modified files.")
#         logging.info("Please review the changes before committing.")
#         return 1  # Return non-zero to abort the commit
#     return 0

# def main():
#     logging.info("\n### Cleaning Files Hook ###")
#     parser = argparse.ArgumentParser()
#     parser.add_argument('--json-config', help='Path to JSON config file', type=str)
#     parser.add_argument('--enforce-all', action='store_true', help='Enforce cleaning all relevant files, not just staged files')
#     args, unknown = parser.parse_known_args()

#     if args.json_config:
#         with open(args.json_config, 'r') as f:
#             config = json.load(f)
#             patterns = config['patterns']
#             include_dirs = config['directories']
#             logging.info(f"Loaded JSON config: {config}")
#     else:
#         logging.error("JSON config file is required.")
#         return 1

#     if include_dirs:
#         expanded_dirs = []
#         for dir_pattern in include_dirs:
#             matching_dirs = glob.glob(dir_pattern)
#             expanded_dirs.extend(matching_dirs)
#         include_dirs = expanded_dirs

#     return clean_files(patterns, include_dirs, args.enforce_all)

# if __name__ == '__main__':
#     logging.basicConfig(filename='pre_commit.log', level=logging.INFO)
#     raise SystemExit(main())

# import re
# import os
# import argparse
# import subprocess
# import glob
# import logging
# import json

# def is_binary_file(filepath):
#     try:
#         with open(filepath, 'rb') as file:
#             for block in iter(lambda: file.read(1024), b''):
#                 if b'\0' in block:
#                     return True
#         return False
#     except Exception as e:
#         logging.error(f"Error checking if file is binary: {e}")
#         return False  # Assume non-binary on error

# def should_skip_file(filepath):
#     # Skip JSON and YAML configuration files
#     if filepath.endswith('.json') or filepath.endswith('.yaml') or filepath.endswith('.yml'):
#         logging.info(f"Skipping configuration file: {filepath}")
#         return True
#     return False

# def clean_file(filepath, patterns):
#     if is_binary_file(filepath):
#         logging.info(f"Skipping binary file: {filepath}")
#         return False

#     if should_skip_file(filepath):
#         return False
    
#     try:
#         with open(filepath, 'r', encoding='utf-8') as file:
#             content = file.read()

#         logging.info(f"Original content of {filepath}:\n{content[:200]}")  # Show first 200 characters for brevity

#         cleaned_content = content
#         for pattern, options in patterns.items():
#             replacement = options["replacement"]
#             inplace = options.get("inplace", False)
            
#             if inplace:
#                 # Pattern to match the entire path up to the file name and extension
#                 flexible_pattern = re.compile(
#                     rf'({re.escape(pattern)})([^\s\'"]*\.[^\s\'"]+)',
#                     re.MULTILINE
#                 )
#             else:
#                 flexible_pattern = re.compile(
#                     rf'(?P<key>{pattern})(\s*=\s*)(?P<value>[^\n]*)',
#                     re.MULTILINE
#                 )

#             matches = flexible_pattern.findall(content)
#             if matches:
#                 logging.info(f"Pattern '{pattern}' found in {filepath}: {matches}")
#             else:
#                 logging.info(f"Pattern '{pattern}' not found in {filepath}")

#             def replace_value(match):
#                 if inplace:
#                     # Replace the full path except the last part (filename.extension)
#                     original_path = match.group(0)
#                     filename = os.path.basename(match.group(2))
#                     new_path = os.path.join(replacement, filename)
#                     logging.info(f"Replacing in-place '{original_path}' with '{new_path}'")
#                     return new_path
#                 else:
#                     key = match.group('key')
#                     logging.info(f"Replacing value for key '{key}' with '{replacement}'")
#                     return f"{key} = {replacement}"

#             cleaned_content = flexible_pattern.sub(replace_value, cleaned_content)

#         if content != cleaned_content:
#             logging.info(f"Modified content of {filepath}:\n{cleaned_content[:200]}")  # Show first 200 characters for brevity
#             with open(filepath, 'w', encoding='utf-8') as file:
#                 file.write(cleaned_content)
#             logging.info(f"File modified: {filepath}")
#             return True
#         else:
#             logging.info(f"No changes needed for file: {filepath}")
#             return False

#     except Exception as e:
#         logging.error(f"Error cleaning file {filepath}: {e}")
#         return False


# def clean_files(patterns, include_dirs=None, enforce_all=False):
#     if enforce_all:
#         all_files = []
#         for root, _, files in os.walk('.'):
#             for file in files:
#                 filepath = os.path.join(root, file)
#                 if include_dirs:
#                     if any(os.path.abspath(filepath).startswith(os.path.abspath(include_dir)) for include_dir in include_dirs):
#                         all_files.append(filepath)
#                 else:
#                     all_files.append(filepath)
#         relevant_files = all_files
#     else:
#         relevant_files = subprocess.check_output(['git', 'diff', '--cached', '--name-only']).decode().splitlines()

#     modified_files = []
#     for filepath in relevant_files:
#         if os.path.exists(filepath):
#             if clean_file(filepath, patterns):
#                 modified_files.append(filepath)
    
#     if modified_files:
#         subprocess.check_call(["git", "add"] + modified_files)
#         logging.info(f"Re-staged modified files.")
#         logging.info("Please review the changes before committing.")
#         return 1  # Return non-zero to abort the commit
#     return 0

# def main():
#     logging.info("\n### Cleaning Files Hook ###")
#     parser = argparse.ArgumentParser()
#     parser.add_argument('--json-config', help='Path to JSON config file', type=str)
#     parser.add_argument('--enforce-all', action='store_true', help='Enforce cleaning all relevant files, not just staged files')
#     args, unknown = parser.parse_known_args()

#     if args.json_config:
#         with open(args.json_config, 'r') as f:
#             config = json.load(f)
#             patterns = config['patterns']
#             include_dirs = config['directories']
#             logging.info(f"Loaded JSON config: {config}")
#     else:
#         logging.error("JSON config file is required.")
#         return 1

#     if include_dirs:
#         expanded_dirs = []
#         for dir_pattern in include_dirs:
#             matching_dirs = glob.glob(dir_pattern)
#             expanded_dirs.extend(matching_dirs)
#         include_dirs = expanded_dirs

#     return clean_files(patterns, include_dirs, args.enforce_all)

# if __name__ == '__main__':
#     logging.basicConfig(filename='pre_commit.log', level=logging.INFO)
#     raise SystemExit(main())

# import re
# import os
# import argparse
# import subprocess
# import glob
# import logging
# import json

# def is_binary_file(filepath):
#     try:
#         with open(filepath, 'rb') as file:
#             for block in iter(lambda: file.read(1024), b''):
#                 if b'\0' in block:
#                     return True
#         return False
#     except Exception as e:
#         logging.error(f"Error checking if file is binary: {e}")
#         return False  # Assume non-binary on error

# def should_skip_file(filepath):
#     # Skip JSON and YAML configuration files
#     if filepath.endswith('.json') or filepath.endswith('.yaml') or filepath.endswith('.yml'):
#         logging.info(f"Skipping configuration file: {filepath}")
#         return True
#     return False

# def clean_file(filepath, patterns):
#     if is_binary_file(filepath):
#         logging.info(f"Skipping binary file: {filepath}")
#         return False

#     if should_skip_file(filepath):
#         return False
    
#     try:
#         with open(filepath, 'r', encoding='utf-8') as file:
#             content = file.read()

#         logging.info(f"Original content of {filepath}:\n{content[:200]}")  # Show first 200 characters for brevity

#         cleaned_content = content
#         for pattern, options in patterns.items():
#             replacement = options["replacement"]
#             inplace = options.get("inplace", False)
#             case_sensitive = options.get("case_sensitive", True)
            
#             # Determine regex flags based on case sensitivity
#             flags = re.MULTILINE
#             if not case_sensitive:
#                 flags |= re.IGNORECASE
            
#             if inplace:
#                 # Pattern to match the entire path up to the file name and extension
#                 flexible_pattern = re.compile(
#                     rf'({re.escape(pattern)})([^\s\'"]*\.[^\s\'"]+)',
#                     flags
#                 )
#             else:
#                 flexible_pattern = re.compile(
#                     rf'(?P<key>{pattern})(\s*=\s*)(?P<value>[^\n]*)',
#                     flags
#                 )

#             matches = flexible_pattern.findall(content)
#             if matches:
#                 logging.info(f"Pattern '{pattern}' found in {filepath}: {matches}")
#             else:
#                 logging.info(f"Pattern '{pattern}' not found in {filepath}")

#             def replace_value(match):
#                 if inplace:
#                     # Replace the full path except the last part (filename.extension)
#                     original_path = match.group(0)
#                     filename = os.path.basename(match.group(2))
#                     new_path = os.path.join(replacement, filename)
#                     logging.info(f"Replacing in-place '{original_path}' with '{new_path}'")
#                     return new_path
#                 else:
#                     key = match.group('key')
#                     logging.info(f"Replacing value for key '{key}' with '{replacement}'")
#                     return f"{key} = {replacement}"

#             cleaned_content = flexible_pattern.sub(replace_value, cleaned_content)

#         if content != cleaned_content:
#             logging.info(f"Modified content of {filepath}:\n{cleaned_content[:200]}")  # Show first 200 characters for brevity
#             with open(filepath, 'w', encoding='utf-8') as file:
#                 file.write(cleaned_content)
#             logging.info(f"File modified: {filepath}")
#             return True
#         else:
#             logging.info(f"No changes needed for file: {filepath}")
#             return False

#     except Exception as e:
#         logging.error(f"Error cleaning file {filepath}: {e}")
#         return False


# def clean_files(patterns, include_dirs=None, enforce_all=False):
#     if enforce_all:
#         all_files = []
#         for root, _, files in os.walk('.'):
#             for file in files:
#                 filepath = os.path.join(root, file)
#                 if include_dirs:
#                     if any(os.path.abspath(filepath).startswith(os.path.abspath(include_dir)) for include_dir in include_dirs):
#                         all_files.append(filepath)
#                 else:
#                     all_files.append(filepath)
#         relevant_files = all_files
#     else:
#         relevant_files = subprocess.check_output(['git', 'diff', '--cached', '--name-only']).decode().splitlines()

#     modified_files = []
#     for filepath in relevant_files:
#         if os.path.exists(filepath):
#             if clean_file(filepath, patterns):
#                 modified_files.append(filepath)
    
#     if modified_files:
#         subprocess.check_call(["git", "add"] + modified_files)
#         logging.info(f"Re-staged modified files.")
#         logging.info("Please review the changes before committing.")
#         return 1  # Return non-zero to abort the commit
#     return 0

# def main():
#     logging.info("\n### Cleaning Files Hook ###")
#     parser = argparse.ArgumentParser()
#     parser.add_argument('--json-config', help='Path to JSON config file', type=str)
#     parser.add_argument('--enforce-all', action='store_true', help='Enforce cleaning all relevant files, not just staged files')
#     args, unknown = parser.parse_known_args()

#     if args.json_config:
#         with open(args.json_config, 'r') as f:
#             config = json.load(f)
#             patterns = config['patterns']
#             include_dirs = config['directories']
#             logging.info(f"Loaded JSON config: {config}")
#     else:
#         logging.error("JSON config file is required.")
#         return 1

#     if include_dirs:
#         expanded_dirs = []
#         for dir_pattern in include_dirs:
#             matching_dirs = glob.glob(dir_pattern)
#             expanded_dirs.extend(matching_dirs)
#         include_dirs = expanded_dirs

#     return clean_files(patterns, include_dirs, args.enforce_all)

# if __name__ == '__main__':
#     logging.basicConfig(filename='pre_commit.log', level=logging.INFO)
#     raise SystemExit(main())


# import re
# import os
# import argparse
# import subprocess
# import glob
# import logging
# import json

# def is_binary_file(filepath):
#     try:
#         with open(filepath, 'rb') as file:
#             for block in iter(lambda: file.read(1024), b''):
#                 if b'\0' in block:
#                     return True
#         return False
#     except Exception as e:
#         logging.error(f"Error checking if file is binary: {e}")
#         return False  # Assume non-binary on error

# def clean_file(filepath, patterns):
#     # Skip .json and .yaml files
#     if filepath.endswith(('.json', '.yaml', '.yml')):
#         logging.info(f"Skipping file: {filepath}")
#         return False

#     if is_binary_file(filepath):
#         logging.info(f"Skipping binary file: {filepath}")
#         return False
    
#     try:
#         with open(filepath, 'r', encoding='utf-8') as file:
#             content = file.read()

#         logging.info(f"Original content of {filepath}:\n{content[:200]}")  # Show first 200 characters for brevity

#         cleaned_content = content
#         for pattern, options in patterns.items():
#             replacement = options.get("replacement")
#             inplace = options.get("inplace", False)
#             case_sensitive = options.get("case_sensitive", True)

#             # Adjust regex pattern for case sensitivity
#             flags = 0 if case_sensitive else re.IGNORECASE

#             if inplace:
#                 # Pattern for matching and replacing entire paths (inplace)
#                 flexible_pattern = re.compile(
#                     rf'(?P<path>{pattern}.*?)(?P<filename>[^/\\]+$)',
#                     flags
#                 )
#                 def replace_path(match):
#                     filename = match.group('filename')
#                     new_path = os.path.join(replacement, filename)
#                     logging.info(f"Replacing path: {match.group(0)} with {new_path}")
#                     return new_path

#                 cleaned_content = flexible_pattern.sub(replace_path, cleaned_content)
#             else:
#                 # Pattern for matching variable assignment
#                 assignment_pattern = re.compile(
#                     rf'(?P<key>{pattern})(\s*=\s*)(?P<value>[^\n]*)',
#                     flags
#                 )
#                 def replace_value(match):
#                     key = match.group('key')
#                     logging.info(f"Replacing value for key '{key}' with {replacement}")
#                     return f"{key} = {replacement}"

#                 cleaned_content = assignment_pattern.sub(replace_value, cleaned_content)

#         if content != cleaned_content:
#             logging.info(f"Modified content of {filepath}:\n{cleaned_content[:200]}")  # Show first 200 characters for brevity
#             with open(filepath, 'w', encoding='utf-8') as file:
#                 file.write(cleaned_content)
#             logging.info(f"File modified: {filepath}")
#             return True
#         else:
#             logging.info(f"No changes needed for file: {filepath}")
#             return False

#     except Exception as e:
#         logging.error(f"Error cleaning file {filepath}: {e}")
#         return False


# def clean_files(patterns, include_dirs=None, enforce_all=False):
#     if enforce_all:
#         all_files = []
#         for root, _, files in os.walk('.'):
#             for file in files:
#                 filepath = os.path.join(root, file)
#                 if include_dirs:
#                     if any(os.path.abspath(filepath).startswith(os.path.abspath(include_dir)) for include_dir in include_dirs):
#                         all_files.append(filepath)
#                 else:
#                     all_files.append(filepath)
#         relevant_files = all_files
#     else:
#         relevant_files = subprocess.check_output(['git', 'diff', '--cached', '--name-only']).decode().splitlines()

#     modified_files = []
#     for filepath in relevant_files:
#         if os.path.exists(filepath):
#             if clean_file(filepath, patterns):
#                 modified_files.append(filepath)
    
#     if modified_files:
#         subprocess.check_call(["git", "add"] + modified_files)
#         logging.info(f"Re-staged modified files.")
#         logging.info("Please review the changes before committing.")
#         return 1  # Return non-zero to abort the commit
#     return 0

# def main():
#     logging.info("\n### Cleaning Files Hook ###")
#     parser = argparse.ArgumentParser()
#     parser.add_argument('--json-config', help='Path to JSON config file', type=str)
#     parser.add_argument('--enforce-all', action='store_true', help='Enforce cleaning all relevant files, not just staged files')
#     args, unknown = parser.parse_known_args()

#     if args.json_config:
#         with open(args.json_config, 'r') as f:
#             config = json.load(f)
#             patterns = config['patterns']
#             include_dirs = config['directories']
#             logging.info(f"Loaded JSON config: {config}")
#     else:
#         logging.error("JSON config file is required.")
#         return 1

#     if include_dirs:
#         expanded_dirs = []
#         for dir_pattern in include_dirs:
#             matching_dirs = glob.glob(dir_pattern)
#             expanded_dirs.extend(matching_dirs)
#         include_dirs = expanded_dirs

#     return clean_files(patterns, include_dirs, args.enforce_all)

# if __name__ == '__main__':
#     logging.basicConfig(filename='pre_commit.log', level=logging.INFO)
#     raise SystemExit(main())

import re
import os
import argparse
import subprocess
import glob
import logging
import json

def is_binary_file(filepath):
    try:
        with open(filepath, 'rb') as file:
            for block in iter(lambda: file.read(1024), b''):
                if b'\0' in block:
                    return True
        return False
    except Exception as e:
        logging.error(f"Error checking if file is binary: {e}")
        return False  # Assume non-binary on error

def clean_file(filepath, patterns):
    # Skip .json and .yaml files
    if filepath.endswith(('.json', '.yaml', '.yml')):
        logging.info(f"Skipping file: {filepath}")
        return False

    if is_binary_file(filepath):
        logging.info(f"Skipping binary file: {filepath}")
        return False
    
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()

        logging.info(f"Original content of {filepath}:\n{content[:200]}")  # Show first 200 characters for brevity

        cleaned_content = content
        for pattern, options in patterns.items():
            replacement = options.get("replacement")
            inplace = options.get("inplace", False)
            case_sensitive = options.get("case_sensitive", True)

            # Adjust regex pattern for case sensitivity
            flags = 0 if case_sensitive else re.IGNORECASE

            if inplace:
                # Pattern for matching and replacing specific paths
                flexible_pattern = re.compile(
                    rf'\b{re.escape(pattern)}\b',
                    flags
                )
                def replace_path(match):
                    # Replace the entire path with the replacement directory and the original filename
                    filename = os.path.basename(match.group(0))
                    new_path = os.path.join(replacement, filename)
                    logging.info(f"Replacing path: {match.group(0)} with {new_path}")
                    return new_path

                cleaned_content = flexible_pattern.sub(replace_path, cleaned_content)
            else:
                # Pattern for matching variable assignment with word boundaries to avoid partial matches
                assignment_pattern = re.compile(
                    rf'\b(?P<key>{re.escape(pattern)})\b(\s*=\s*)(?P<value>[^\n]*)',
                    flags
                )
                def replace_value(match):
                    key = match.group('key')
                    logging.info(f"Replacing value for key '{key}' with {replacement}")
                    return f"{key} = {replacement}"

                cleaned_content = assignment_pattern.sub(replace_value, cleaned_content)

        if content != cleaned_content:
            logging.info(f"Modified content of {filepath}:\n{cleaned_content[:200]}")  # Show first 200 characters for brevity
            with open(filepath, 'w', encoding='utf-8') as file:
                file.write(cleaned_content)
            logging.info(f"File modified: {filepath}")
            return True
        else:
            logging.info(f"No changes needed for file: {filepath}")
            return False

    except Exception as e:
        logging.error(f"Error cleaning file {filepath}: {e}")
        return False


def clean_files(patterns, include_dirs=None, enforce_all=False):
    if enforce_all:
        all_files = []
        for root, _, files in os.walk('.'):
            for file in files:
                filepath = os.path.join(root, file)
                if include_dirs:
                    if any(os.path.abspath(filepath).startswith(os.path.abspath(include_dir)) for include_dir in include_dirs):
                        all_files.append(filepath)
                else:
                    all_files.append(filepath)
        relevant_files = all_files
    else:
        relevant_files = subprocess.check_output(['git', 'diff', '--cached', '--name-only']).decode().splitlines()

    modified_files = []
    for filepath in relevant_files:
        if os.path.exists(filepath):
            if clean_file(filepath, patterns):
                modified_files.append(filepath)
    
    if modified_files:
        subprocess.check_call(["git", "add"] + modified_files)
        logging.info(f"Re-staged modified files.")
        logging.info("Please review the changes before committing.")
        return 1  # Return non-zero to abort the commit
    return 0

def main():
    logging.info("\n### Cleaning Files Hook ###")
    parser = argparse.ArgumentParser()
    parser.add_argument('--json-config', help='Path to JSON config file', type=str)
    parser.add_argument('--enforce-all', action='store_true', help='Enforce cleaning all relevant files, not just staged files')
    args, unknown = parser.parse_known_args()

    if args.json_config:
        with open(args.json_config, 'r') as f:
            config = json.load(f)
            patterns = config['patterns']
            include_dirs = config['directories']
            logging.info(f"Loaded JSON config: {config}")
    else:
        logging.error("JSON config file is required.")
        return 1

    if include_dirs:
        expanded_dirs = []
        for dir_pattern in include_dirs:
            matching_dirs = glob.glob(dir_pattern)
            expanded_dirs.extend(matching_dirs)
        include_dirs = expanded_dirs

    return clean_files(patterns, include_dirs, args.enforce_all)

if __name__ == '__main__':
    logging.basicConfig(filename='pre_commit.log', level=logging.INFO)
    raise SystemExit(main())

# import re
# import os
# import argparse
# import subprocess
# import glob
# import json

# def is_binary_file(filepath):
#   try:
#       with open(filepath, 'rb') as file:
#           for block in iter(lambda: file.read(1024), b''):
#               if b'\0' in block:
#                   return True
#       return False
#   except Exception as e:
#       print(f"Error checking if file is binary: {e}")
#       return False  # Assume non-binary on error

# def clean_file(filepath, patterns):
#   # Skip .json and .yaml files
#   if filepath.endswith(('.json', '.yaml', '.yml')):
#       print(f"Skipping file: {filepath}")
#       return False

#   if is_binary_file(filepath):
#       print(f"Skipping binary file: {filepath}")
#       return False
  
#   try:
#       with open(filepath, 'r', encoding='utf-8') as file:
#           content = file.read()

#       print(f"Cleaning file: {filepath}")

#       cleaned_content = content
#       for pattern, options in patterns.items():
#           replacement = options.get("replacement")
#           inplace = options.get("inplace", False)
#           case_sensitive = options.get("case_sensitive", True)

#           flags = 0 if case_sensitive else re.IGNORECASE

#           if inplace:
#               flexible_pattern = re.compile(rf'\b{re.escape(pattern)}\b', flags)
#               def replace_path(match):
#                   filename = os.path.basename(match.group(0))
#                   new_path = os.path.join(replacement, filename)
#                   print(f"Replacing path: {match.group(0)} with {new_path}")
#                   return new_path

#               cleaned_content = flexible_pattern.sub(replace_path, cleaned_content)
#           else:
#               assignment_pattern = re.compile(rf'\b(?P<key>{re.escape(pattern)})\b(\s*=\s*)(?P<value>[^\n]*)', flags)
#               def replace_value(match):
#                   key = match.group('key')
#                   print(f"Replacing value for key '{key}' with {replacement}")
#                   return f"{key} = {replacement}"

#               cleaned_content = assignment_pattern.sub(replace_value, cleaned_content)

#       if content != cleaned_content:
#           with open(filepath, 'w', encoding='utf-8') as file:
#               file.write(cleaned_content)
#           print(f"File modified: {filepath}")
#           return True
#       else:
#           print(f"No changes needed for file: {filepath}")
#           return False

#   except Exception as e:
#       print(f"Error cleaning file {filepath}: {e}")
#       return False

# def clean_files(patterns, include_dirs=None, enforce_all=False):
#   if enforce_all:
#       all_files = []
#       for root, _, files in os.walk('.'):
#           for file in files:
#               filepath = os.path.join(root, file)
#               if include_dirs:
#                   if any(os.path.abspath(filepath).startswith(os.path.abspath(include_dir)) for include_dir in include_dirs):
#                       all_files.append(filepath)
#               else:
#                   all_files.append(filepath)
#       relevant_files = all_files
#   else:
#       relevant_files = subprocess.check_output(['git', 'diff', '--cached', '--name-only']).decode().splitlines()

#   modified_files = []
#   for filepath in relevant_files:
#       if os.path.exists(filepath):
#           if clean_file(filepath, patterns):
#               modified_files.append(filepath)
  
#   if modified_files:
#       subprocess.check_call(["git", "add"] + modified_files)
#       print(f"Re-staged modified files: {', '.join(modified_files)}")
#       print("Please review the changes before committing.")
#   else:
#       print("No files were modified.")

#   return 0  # Always allow the commit to proceed

# def main():
#   print("\n### Cleaning Files Hook ###")
#   parser = argparse.ArgumentParser()
#   parser.add_argument('--json-config', help='Path to JSON config file', type=str)
#   parser.add_argument('--enforce-all', action='store_true', help='Enforce cleaning all relevant files, not just staged files')
#   args, unknown = parser.parse_known_args()

#   if args.json_config:
#       with open(args.json_config, 'r') as f:
#           config = json.load(f)
#           patterns = config['patterns']
#           include_dirs = config['directories']
#           print(f"Loaded JSON config: {config}")
#   else:
#       print("JSON config file is required.")
#       return 0  # Still allow commit to proceed

#   if include_dirs:
#       expanded_dirs = []
#       for dir_pattern in include_dirs:
#           matching_dirs = glob.glob(dir_pattern)
#           expanded_dirs.extend(matching_dirs)
#       include_dirs = expanded_dirs

#   return clean_files(patterns, include_dirs, args.enforce_all)

# if __name__ == '__main__':
#   raise SystemExit(main())

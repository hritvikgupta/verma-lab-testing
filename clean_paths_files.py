import re
import os
import argparse
import subprocess

def clean_file(file_path):
  # Skip the clean_paths_files.py script itself
  if file_path.endswith("clean_paths_files.py"):
      return False

  print(f"Cleaning file: {file_path}")
  try:
      with open(file_path, 'r', encoding='utf-8') as file:
          content = file.read()

      # Define the pattern and replacement
      pattern = r'/PMBB/file_param_name.extension'
      replacement = 'dummy/file_param_name.extension'

      # Perform the replacement
      cleaned_content = re.sub(pattern, replacement, content)

      if content != cleaned_content:
          # Write the cleaned content back to the file
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

def clean_staged_files():
  # Get list of staged files
  staged_files = subprocess.check_output(['git', 'diff', '--cached', '--name-only']).decode().splitlines()
  
  modified_files = []
  for file_path in staged_files:
      if clean_file(file_path):
          modified_files.append(file_path)
  
  if modified_files:
      subprocess.check_call(["git", "add"] + modified_files)
      print("Re-staged modified files.")

def main(argv=None):
  print("Running clean_paths_files.py")
  clean_staged_files()
  print("Finished running clean_paths_files.py")

if __name__ == '__main__':
  import sys
  sys.exit(main())
import re
import os
import argparse
import subprocess
import sys

def clean_file_content(content):
  pattern = r'/PMBB/file_param_name.extension'
  replacement = 'dummy/file_param_name.extension'
  return re.sub(pattern, replacement, content)

def clean_file(file_path):
  print(f"Attempting to clean file: {file_path}", file=sys.stderr)
  try:
      with open(file_path, 'r', encoding='utf-8') as file:
          content = file.read()

      cleaned_content = clean_file_content(content)

      if content != cleaned_content:
          with open(file_path, 'w', encoding='utf-8') as file:
              file.write(cleaned_content)
          print(f"Cleaned file: {file_path}", file=sys.stderr)
          return True
      else:
          print(f"No changes needed for file: {file_path}", file=sys.stderr)
          return False

  except Exception as e:
      print(f"Error cleaning file: {e}", file=sys.stderr)
      return False

def clean_directory(directory_path):
  print(f"Cleaning files in directory: {directory_path}", file=sys.stderr)
  
  modified_files = []
  for root, _, files in os.walk(directory_path):
      for file in files:
          file_path = os.path.join(root, file)
          if clean_file(file_path):
              modified_files.append(file_path)
  
  if modified_files:
      subprocess.check_call(["git", "add"] + modified_files)
      print(f"Re-staged modified files: {modified_files}", file=sys.stderr)
  
  return modified_files

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('directory', help='Directory to clean (e.g., PMBB)')
  args, unknown = parser.parse_known_args()

  print(f"Starting cleaning process for directory: {args.directory}", file=sys.stderr)
  modified_files = clean_directory(args.directory)
  
  if modified_files:
      print("Files cleaned and re-staged. Please review the changes before pushing.", file=sys.stderr)
  else:
      print("No files needed cleaning.", file=sys.stderr)

if __name__ == '__main__':
  main()
import re
import os
import argparse
import subprocess
import sys
import tempfile
import shutil

def clean_file_content(content):
  pattern = r'/PMBB/file_param_name.extension'
  replacement = 'dummy/file_param_name.extension'
  return re.sub(pattern, replacement, content)

def create_temp_cleaned_file(file_path):
  print(f"Attempting to clean file: {file_path}", file=sys.stderr)
  try:
      with open(file_path, 'r', encoding='utf-8') as file:
          content = file.read()

      cleaned_content = clean_file_content(content)

      if content != cleaned_content:
          temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8')
          temp_file.write(cleaned_content)
          temp_file.close()
          print(f"Created cleaned temporary file for: {file_path}", file=sys.stderr)
          return temp_file.name
      else:
          print(f"No changes needed for file: {file_path}", file=sys.stderr)
          return None

  except Exception as e:
      print(f"Error cleaning file: {e}", file=sys.stderr)
      return None

def clean_directory(directory_path):
  print(f"Cleaning files in directory: {directory_path}", file=sys.stderr)
  
  temp_files = []
  for root, _, files in os.walk(directory_path):
      for file in files:
          file_path = os.path.join(root, file)
          temp_file = create_temp_cleaned_file(file_path)
          if temp_file:
              temp_files.append((file_path, temp_file))
  
  return temp_files

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('directory', help='Directory to clean (e.g., PMBB)')
  args, unknown = parser.parse_known_args()

  print(f"Starting cleaning process for directory: {args.directory}", file=sys.stderr)
  temp_files = clean_directory(args.directory)
  
  if temp_files:
      print("Temporary cleaned files created. Updating index for push...", file=sys.stderr)
      for original, temp in temp_files:
          subprocess.call(['git', 'update-index', '--cacheinfo', '100644', 
                           subprocess.check_output(['git', 'hash-object', '-w', temp]).decode().strip(), 
                           original])
      
      print("Cleaned files staged for push. Original files remain unchanged.", file=sys.stderr)
      print("Push can proceed. Local files will remain unchanged.", file=sys.stderr)
      
      # Clean up temporary files
      for _, temp in temp_files:
          os.unlink(temp)
  else:
      print("No files needed cleaning.", file=sys.stderr)

if __name__ == '__main__':
  main()
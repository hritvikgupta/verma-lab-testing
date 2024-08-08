import re
import argparse

def clean_file(file_path):
  print(f"Cleaning file: {file_path}")
  try:
      with open(file_path, 'r', encoding='utf-8') as file:
          content = file.read()

      pattern = r'"/PMBB/file_param_name.extension"'
      replacement = '"dummy/file_param_name.extension"'
      cleaned_content = re.sub(pattern, replacement, content)

      with open(file_path, 'w', encoding='utf-8') as file:
          file.write(cleaned_content)

  except Exception as e:
      print(f"Error cleaning file: {e}")

def main(argv=None):
  print("Running clean_config_files.py")
  parser = argparse.ArgumentParser()
  parser.add_argument('filenames', nargs='*', help='Filenames to clean')
  args = parser.parse_args(argv)

  for file_path in args.filenames:
      clean_file(file_path)

  print("Finished running clean_config_files.py")

if __name__ == '__main__':
  import sys
  sys.exit(main())
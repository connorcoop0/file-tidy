import hashlib
from pathlib import Path
import argparse
import os
import shutil

# instantiate lists
hash_list = []
duplicate_files = []

# set up argument parsing
parser = argparse.ArgumentParser(description="Organize directories, find and deleteDuplicate Files")
# directory path argument
parser.add_argument('directory_path', nargs='?', metavar='directory_path', default=os.getcwd(), help='Enter the target directory path, default is cwd')
# Groups
fo_group = parser.add_argument_group('File organization settings')
dedupe_group = parser.add_argument_group('De-Deuplication settings')

# DeDuplication settings
dedupe_group.add_argument('-d', '--dedupe', action='store_true', help="De-duplication mode")
dedupe_group.add_argument('-r', '--recursive', action='store_true', help="Recursive file search mode")
dedupe_group.add_argument('-f', '--file-by-file', action='store_true', help="file-by-file delete confirmation mode")
dedupe_group.add_argument('-e', '--extension', metavar='ext', default='', help="Optional file extension filter (e.g., 'txt', 'py'). Leave blank to scan all file types.")
dedupe_group.add_argument('-dr', '--dry-run', action='store_true', help="dry simulation run")
dedupe_group.add_argument('-fd', '--force-delete', action='store_true', help="Delete all duplicates without confirmation (DANGEROUS)")

# File organization settings
fo_group.add_argument('-o', '--organize', action='store_true', help="File organization mode")
fo_group.add_argument('-s', '--summary', action='store_true', help="Print a summary of processes executed")

# parse given arguments
args = parser.parse_args()


# ***************************************************************************
# ****************************** DeDuplication ******************************
# *************************************************************************** 
# Deduplication functions
# file hashing
def hashfile(file):
    BUF_SIZE = 65536
    sha256 = hashlib.sha256()

    with open(file, 'rb') as f:
        while chunk := f.read(BUF_SIZE):
            sha256.update(chunk)

    return sha256.hexdigest()

# file by file deletion with confirmation
def confirm_file_by_file(files):
    for file in files:
        while True:
            prompt = f"Are you sure you want to delete {file} y or n: "
            file_by_file_confirmation = prompt_yes_no(prompt)
            if file_by_file_confirmation == 'y':
                delete_file(file)
                break
            else:
                print("File not deleted!")
                break

# prompts user yes or no based on prompt and returns 'y' or 'n'
def prompt_yes_no(question):
    while True:
        yes_no = input(question)
        if yes_no not in ['y', 'n']:
            print("Must enter 'y' or 'n'")
            continue
        else:
            return yes_no


# delete an individual file
def delete_file(file):
    file.unlink()
    print(f"{file.name} deleted")


# Deletes all files in list
def delete_all(files):
    for file in files:
        delete_file(file)

# simulate file by file deletion with confirmation
def dry_file_by_file(files):
    for file in files:
        while True:
            prompt = f"Are you sure you want to delete {file} y or n: "
            file_by_file_confirmation = prompt_yes_no(prompt)
            if file_by_file_confirmation == 'y':
                dry_delete_file(file)
                break
            else:
                print("File not deleted!")
                break

# simulate deletion of an individual file
def dry_delete_file(file):
    print(f"{file.name} deleted")

# simulate deletion of all files in list
def dry_delete_all(files):
    for file in files:
        dry_delete_file(file)


# set given directory and confirm validity
directory_path = Path(args.directory_path)
if not directory_path.is_dir():
    print("Invalid Path")
    exit()

# DeDupe process
if args.dedupe:
    if args.extension:
        extension = '*.' + args.extension
    else:
        extension = '*'
    if args.recursive:
        files = directory_path.rglob(extension)
    else:
        files = directory_path.glob(extension)
    for file in files:
        if file.is_file():
            file_hash = hashfile(file)
            if file_hash in hash_list:
                duplicate_files.append(file)
                continue
            hash_list.append(file_hash)

    if duplicate_files: print("Duplicate files were found")
    else: print("No duplicates found")
    for file in duplicate_files:
        print(file.name)

    # --file-by-file
    if args.file_by_file:
        if args.dry_run:
            dry_file_by_file(duplicate_files)
            exit()
        confirm_file_by_file(duplicate_files)

    # --force-delete
    elif args.force_delete:
        # Final confirmation prompt
        delete_all_confirmation = prompt_yes_no("Are you sure you want to delete all duplicate files? (DANGEROUS)")
        # Check for --dry-run
        if delete_all_confirmation == 'y' and args.dry_run:
            dry_delete_all(duplicate_files)
        elif delete_all_confirmation == 'y' and not args.dry_run:
            delete_all(duplicate_files)



# ***************************************************************************
# **************************** File-Organization ****************************
# ***************************************************************************
# global list of the sorted directory names
directories = ["Documents_Sorted", "Spreadsheets_Sorted", "Images_Sorted", "Audio_Sorted", "Video_Sorted", "Scripts_Sorted", "Archives_Sorted", "Other_Sorted"]

# File sorting Functions
# Gets all file names
def get_dir_files(file_path):
    file_list = []
    for files in os.listdir(file_path):
        file_name, file_extension = os.path.splitext(files)
        if file_extension:
            file_list.append(file_name+file_extension)
    return file_list
            
def create_sorted_directories(file_path):
    for directory in directories:
        try:
            os.mkdir(os.path.join(file_path, directory))
        except FileExistsError:
            pass

def remove_empty_directories(file_path):
    for directory in directories:
        try:
            os.rmdir(os.path.join(file_path, directory))
        except OSError:
            pass

# Displays amount of files moved to target directory
def sorting_summary(documents_moved, target_directory):
    if documents_moved > 0:
        print(documents_moved, "files moved to", str(target_directory))

# Organization process
if args.organize:
    # Initializing dictionary for summary
    files_moved = {"Documents Moved": 0,
                   "Spreadsheets Moved": 0,
                   "Images Moved": 0,
                   "Audio Moved": 0,
                   "Videos Moved": 0,
                   "Scripts Moved": 0,
                   "Archives Moved": 0,
                   "Other Moved": 0}

    # creating sorted directories
    create_sorted_directories(directory_path)

    # get list of files in directory
    files_in_dir = get_dir_files(directory_path)
    # Moving of files
    for file in files_in_dir:
        file_name, file_extension = os.path.splitext(file)
        file_extension = file_extension.lower()
        file_full_path = os.path.join(directory_path, file)
        if not os.path.isfile(file_full_path):
            continue  # Skip if not a file
        
        if file_extension in [".docx", ".doc", ".pdf", ".rtf", ".txt"]:
            shutil.move(file_full_path, os.path.join(directory_path, "Documents_Sorted"))
            files_moved["Documents Moved"] += 1

        elif file_extension in [".csv", ".xlsx", ".xsl", ".ods"]:
            shutil.move(file_full_path, os.path.join(directory_path, "Spreadsheets_Sorted"))
            files_moved["Spreadsheets Moved"] += 1
            
        elif file_extension in [".jpg", ".jpeg", ".png", ".webp"]:
            shutil.move(file_full_path, os.path.join(directory_path, "Images_Sorted"))
            files_moved["Images Moved"] += 1

        elif file_extension in [".mp3", ".wav", ".aud", ".ogg", ".m4a", ".wma"]:
            shutil.move(file_full_path, os.path.join(directory_path, "Audio_Sorted"))
            files_moved["Audio Moved"] += 1

        elif file_extension in [".mov", ".mp4", ".mkv", ".wmv", ".webm"]:
            shutil.move(file_full_path, os.path.join(directory_path, "Video_Sorted"))
            files_moved["Videos Moved"] += 1

        elif file_extension in [".py", ".c", ".cpp", ".h", ".r"]:
            shutil.copy(file_full_path, os.path.join(directory_path, "Scripts_Sorted"))
            files_moved["Scripts Moved"] += 1

        elif file_extension in [".zip", ".rar", ".tar", ".gz", ".7z"]:
            shutil.move(file_full_path, os.path.join(directory_path, "Archives_Sorted"))
            files_moved["Archives Moved"] += 1

        else:
            shutil.copy(file_full_path, os.path.join(directory_path, "Other_Sorted"))
            files_moved["Other Moved"] += 1
    
    # remove the newly created unused/empty directories
    remove_empty_directories(directory_path)

    # print summary of movement
    if args.summary:
        for element in files_moved:
            file_count = int(files_moved.get(element))
            if file_count > 0:
                print(f"{element}: {file_count}")


    
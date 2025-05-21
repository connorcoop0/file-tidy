# File Tidy CLI

File Tidy is a Python command-line tool that helps manage cluttered directories by combining two utilities: file deduplication and file organization. It includes safety features like dry-run simulation, extension filtering, and confirmation prompts to prevent accidental data loss.

## Features

- File deduplication based on SHA-256 hashing
- Optional recursive search and extension filtering
- Multiple deletion modes: dry-run, file-by-file confirmation, or force delete
- File organization into categorized folders (Documents, Images, Audio, etc.)
- Optional summary output of organized files
- Built-in protection against empty directory creation and accidental overwrites

## Usage

Deduplicate all files in the current directory:

```
python tidy.py --dedupe
```

Deduplicate all `.txt` files recursively with confirmation:

```
python tidy.py --dedupe --recursive --extension txt --file-by-file
```

Organize files into folders and print a summary:

```
python tidy.py --organize --summary
```

Force delete all detected duplicates without confirmation:

```
python tidy.py --dedupe --force-delete
```

## Arguments

```
positional arguments:
  directory_path         Target directory (default is current working directory)

optional arguments:
  -h, --help             Show help message and exit

File organization settings:
  -o, --organize         Organize files into categorized folders
  -s, --summary          Print a summary of files moved

De-duplication settings:
  -d, --dedupe           Run duplicate detection
  -r, --recursive        Search recursively
  -f, --file-by-file     Confirm each deletion individually
  -e, --extension EXT    Filter files by extension (e.g., txt, py)
  -dr, --dry-run         Simulate actions without modifying files
  -fd, --force-delete    Delete all duplicates without confirmation (use with caution)
```

## Notes

This script is a consolidation of two standalone tools originally created to handle file deduplication and directory organization separately. The merged version provides more flexibility and utility while remaining lightweight and dependency-free.

Requires Python 3.7 or higher.

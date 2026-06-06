#!/usr/bin/env python3
"""
File Organizer

This script automatically organizes files in a designated directory by placing
them into subfolders corresponding to their respective file extensions,
creating new folders as needed to accommodate existing file types and
relocating the files accordingly.

Usage:
    python file_organizer.py [directory_path]

    If no directory_path is provided, the script will use the current
    directory.

"""

import os
import shutil
import sys
from typing import Dict, List, Set, Tuple


def create_type_folders(base_path: str, folder_types: List[str]) -> None:
    """
    Create folders for each file type if they don't already exist.

    Args:
        base_path (str): The base directory where folders will be created or
                         the current directory. Get by the main function
        folder_types (List[str]): List of folder names to create
    """
    for folder in folder_types:
        folder_path = os.path.join(base_path, folder)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print(f"Created folder: {folder}")


def get_file_type_mapping() -> Dict[str, str]:
    """
    Define mapping between file extensions and file destination folders.

    Returns:
        Dict[str, str]: Dictionary mapping file extensions to folder names
        where the files will be moved
    """
    return {
        # Images
        ".jpg": "image_files",
        ".jpeg": "image_files",
        ".png": "image_files",
        ".gif": "image_files",
        ".bmp": "image_files",
        ".svg": "image_files",
        # Documents
        ".pdf": "pdf_files",
        ".docx": "word_files",
        ".doc": "word_files",
        ".xls": "spreadsheet_files",
        ".xlsx": "spreadsheet_files",
        ".txt": "text_files",
        ".md": "markdown_files",
        ".rtf": "text_files",
        # Videos
        ".mp4": "video_files",
        ".mov": "video_files",
        ".avi": "video_files",
        ".mkv": "video_files",
        # Add more mappings as needed
        ".py": "python_files",
        ".sh": "shell_files",
        ".lua": "lua_files",
        ".rb": "ruby_files",
        ".go": "go_files",
    }


def _check_existing_type_files(
    directory_path: str, file_dir_map: Dict[str, str]
) -> Set[str]:
    """
    Check existing files and return set of folders types that need to be
    created

    Args:
        directory_path (str): Path to check files in
        file_dir_map (Dict[str, str]): Mapping of extensions to folders

    Returns:
        Set[str]: Set of needed folder types to create
    """
    folders_to_create = set()

    for filename in os.listdir(directory_path):
        if os.path.isdir(os.path.join(directory_path, filename)):
            continue

        _, extension = os.path.splitext(filename)
        extension = extension.lower()

        if extension in file_dir_map:
            folders_to_create.add(file_dir_map[extension])

    return folders_to_create


def organize_files(directory_path: str) -> Tuple[int, List[str]]:
    """
    Move files in the directory that match their extensions.

    Args:
        directory_path (str): Path to the directory containing files to
        organize

    Returns:
        Tuple[int, List[str]]: Number of files moved and list of skipped files
    """
    # Get mapping of extensions to folders
    file_dir_map = get_file_type_mapping()

    # Get only the needed folders to create for existing files
    folders_to_create = _check_existing_type_files(
        directory_path, file_dir_map)

    # Create only the folders based on the existing files
    create_type_folders(directory_path, list(folders_to_create))

    files_moved = 0
    skipped_files = []

    # Process each file in the directory
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)

        # Skip directories and the script itself
        if os.path.isdir(file_path) or filename == os.path.basename(__file__):
            continue

        # Get the file extension
        _, extension = os.path.splitext(filename)
        extension = (
            extension.lower()
        )  # Convert to lowercase for case-insensitive matching

        # Check if we have a mapping for this extension
        if extension in file_dir_map:
            destination_folder = file_dir_map[extension]
            source_path = os.path.join(directory_path, filename)
            dest_path = os.path.join(
                directory_path, destination_folder, filename
            )

            try:
                # Move the file to its destination folder
                shutil.move(source_path, dest_path)
                files_moved += 1
                print(f"Moved: {filename} -> {destination_folder}/")
            except Exception as e:
                print(f"Error moving {filename}: {str(e)}")
                skipped_files.append(filename)
        else:
            skipped_files.append(filename)

    return files_moved, skipped_files


def main():
    """Main function to run the script."""
    # Determine the directory to organize
    if len(sys.argv) > 1:
        directory = sys.argv[1]
    else:
        directory = os.getcwd()

    # Handle relative paths
    directory = os.path.abspath(directory)

    # Check if directory exists
    if not os.path.isdir(directory):
        print(
            f"Error: Directory '{directory}' does not exist or is not a \
                directory"
        )
        return 1

    print(f"Organizing files in: {directory}")

    try:
        files_moved, skipped_files = organize_files(directory)

        print(f"\nOrganization complete!")
        print(f"Files moved: {files_moved}")

        if skipped_files:
            print(
                f"Files skipped (unknown type or error): {len(skipped_files)}"
            )
            # Uncomment to show skipped files
            # for file in skipped_files:
            #     print(f"  - {file}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())

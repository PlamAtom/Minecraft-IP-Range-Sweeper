import os
import shutil
from datetime import datetime

def show_notice_and_get_confirmation():
    notice = """
Each scanner saves its results to a separate file. Before combining them into a results file, please ensure all scanner windows have finished running. All folders with names like scanner_0–9999 will be deleted for a fresh start. If you want to keep them, please make a backup.

Type 'Proceed' (case-sensitive) to continue, or close this window to cancel.
"""
    print("|"*240)
    print(notice)
    print("_|_"*80)
    user_input = input("Type here: ").strip()
    if user_input != "Proceed":
        print("Operation cancelled by user.")
        exit(0)

def main():
    show_notice_and_get_confirmation()

    # Get the current directory (where this script is run from)
    base_dir = os.path.abspath(os.path.dirname(__file__))

    # Generate output filename with current date and time
    now = datetime.now()
    fname = now.strftime("results_%Y-%m-%d_%H-%M-%S.txt")
    output_file = os.path.join(base_dir, fname)
    merged = []
    total_files = 0

    # Look for folders named scanner_0, scanner_1, ..., scanner_9999 (inclusive)
    for i in range(0, 10000):
        folder_name = f"scanner_{i}"
        folder_path = os.path.join(base_dir, folder_name)
        scan_file_path = os.path.join(folder_path, f"servers_{i}.txt")
        if os.path.isdir(folder_path) and os.path.isfile(scan_file_path):
            with open(scan_file_path, "r", encoding="utf-8") as f:
                lines = [line.strip() for line in f if line.strip()]
                merged.extend(lines)
                total_files += 1

    # Remove duplicates and sort the results
    merged = sorted(set(merged))

    # Write to output file
    with open(output_file, "w", encoding="utf-8") as out:
        for line in merged:
            out.write(line + "\n")

    print(f"Merged {total_files} files into {output_file}.")
    print(f"Total unique servers: {len(merged)}")

    # Delete all folders named scanner_0-scanner_9999 in the current directory
    deleted_folders = []
    for i in range(0, 10000):
        folder_name = f"scanner_{i}"
        folder_path = os.path.join(base_dir, folder_name)
        if os.path.isdir(folder_path):
            try:
                shutil.rmtree(folder_path)
                deleted_folders.append(folder_name)
            except Exception as e:
                print(f"Could not delete folder {folder_name}: {e}")

    print(f"Deleted folders: {', '.join(deleted_folders)}")

if __name__ == "__main__":
    main()

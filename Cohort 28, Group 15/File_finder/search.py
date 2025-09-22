import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List
from config import config

# -------------------------------
# Safe input with quit handling
# -------------------------------


def safe_input(prompt: str) -> str:
    """Prompt user for input with quit option."""
    print("\nEnter 'q'/'quit' to exit the current operation.")
    user_input = input(prompt).strip()
    if user_input.lower() in ("q", "quit"):
        print(" ❌ User has cancelled current operation ❌")
        return "QUIT_SIGNAL"
    return user_input

# -------------------------------
# Search function
# -------------------------------
def search_files():
    """
    Start a search loop:
    - Ask user for query
    - Perform search
    - Show summary
    - Offer options (view results, search again, quit)
    """
    while True:
        query = safe_input("\nEnter file or folder name: ")
        if query == "QUIT_SIGNAL":
            return []  # back to main menu

        print("\n⌚ Searches take approximately 5 - 10mins ⌚")
        print("Enjoy some tea 🍵🫖 while you wait...\n")

        start_time = datetime.now()
        results: List[Dict[str, object]] = []

        root = Path(config["root_path"])
        query_cmp = query if config["case_sensitive"] else query.lower()

        for dirpath, dir_names, filenames in os.walk(root):
            # check directories
            for d in dir_names:
                name_cmp = d if config["case_sensitive"] else d.lower()
                if query_cmp in name_cmp:
                    path_obj = Path(dirpath) / d
                    results.append(get_file_info(path_obj))

            # check files
            for f in filenames:
                name_cmp = f if config["case_sensitive"] else f.lower()
                if query_cmp in name_cmp:
                    path_obj = Path(dirpath) / f
                    results.append(get_file_info(path_obj))

        end_time = datetime.now()
        elapsed = (end_time - start_time).total_seconds()

        print(f"\n✅ Search complete!")
        print(f"Found {len(results)} results in {elapsed:.2f} seconds.")

        # the menu after the search
        while True:
            print("\nWhat would you like to do?")
            print("1. View results")
            print("2. Search again")
            print("3. Return to Main Menu")

            choice = safe_input("Enter choice: ")
            if choice == "QUIT_SIGNAL" or choice == "3":
                return []
            elif choice == "1":
                if len(results) == 0:
                    print("\n No path found")
                else:
                return results
            elif choice == "2":
                break
            else:
                print("Invalid option. Please choose 1, 2, or 3.")

# -------------------------------
# File info helper
# -------------------------------


def get_file_info(path_obj: Path) -> Dict[str, object]:
    """Return dictionary of file/folder info"""
    stats = path_obj.stat()
    return {
        "path": str(path_obj.resolve()),
        "is_directory": path_obj.is_dir(),
        "created": datetime.fromtimestamp(stats.st_ctime).strftime("%Y-%m-%d %H:%M:%S"),
        "modified": datetime.fromtimestamp(stats.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
    }


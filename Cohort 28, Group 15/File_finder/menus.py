from typing import List, Dict
from config import config, set_root_path, toggle_case_sensitive, set_display_size
from search import search_files


#                                     Quit handling input function



def safe_input(prompt: str) -> str:
    """Prompt user for input with quit option."""
    print("\nEnter 'q'/'quit' to exit the current operation.")
    user_input = input(prompt).strip()
    if user_input.lower() in ("q", "quit"):
        print(" ❌ User has cancelled current operation ❌")
        return "QUIT_SIGNAL"
    return user_input


#                                         Results display function



def display_results(results: List[Dict[str, object]]) -> None:
    """Show results page by page with full details"""
    if len(results) == 0:
        print("No results to display.")
        return

    page = 0
    per_page = config["display_size"]

    while True:
        start = page * per_page
        end = start + per_page
        subset = results[start:end]

        print(f"\n--- Results Page {page+1} ---")
        for i, item in enumerate(subset, start + 1):
            print(f"{i}. {item['path']}")
            print(f"   Created: {item['created']}")
            print(f"   Modified: {item['modified']}")
            print(f"   Directory: {item['is_directory']}\n")

        #                                   pagination menu code
        print("Options: ")
        if end < len(results):
            print("N. Next page")
        if page > 0:
            print("P. Previous page")
        print("M. Return to Main Menu")

        choice = safe_input("Enter choice: ")
        if choice == "QUIT_SIGNAL" or choice.lower() == "m":
            return
        elif choice.lower() == "n" and end < len(results):
            page += 1
        elif choice.lower() == "p" and page > 0:
            page -= 1
        else:
            print("Invalid option.")


#                                             Main Menu


def main_menu() -> None:
    """Main interactive loop"""
    while True:
        print("\n=== File Finder Main Menu ===")
        print("1. Search for a File/Folder")
        print("2. View Current Settings")
        print("3. Edit Settings")
        print("4. Exit")

        choice = safe_input("Choose an option: ")
        if choice == "QUIT_SIGNAL":
            print(" Goodbye! ")
            break

        try:
            choice = int(choice)
        except ValueError:
            print("⚠️ Invalid input! Enter a number.")
            continue

        if choice == 1:
            results = search_files()
            if results and results != "QUIT_SIGNAL":
                display_results(results)

        elif choice == 2:
            view_settings_menu()

        elif choice == 3:
            edit_settings_menu()

        elif choice == 4:
            print("Goodbye!")
            break
        else:
            print("⚠️  Invalid choice.\nPlease select a number from the ones provided")


#                                          View Settings Menu
# 


def view_settings_menu() -> None:
    """Menu for viewing settings with styled option/value output"""
    while True:
        print("\n--- View Current Settings ---\nSelect from the following menu")
        print("1. Search Folder")
        print("2. Search Display Size")
        print("3. Case Sensitive")
        print("4. Return to Main Menu")

        choice = safe_input("Choose an option: ")
        if choice == "QUIT_SIGNAL":
            return

        try:
            choice = int(choice)
        except ValueError:
            print("⚠️ Invalid menu choice! Please enter a number 1–4.")
            continue

        if choice == 1:
            print("\n🔎 Search Folder:")
            print(f"   {config['root_path']}")
        elif choice == 2:
            print("\n📄 Search Display Size:")
            print(f"   {config['display_size']}")
        elif choice == 3:
            print("\n🔠 Case Sensitive:")
            print(f"   {config['case_sensitive']}")
        elif choice == 4:
            return
        else:
            print("⚠️ Invalid menu choice! Please select 1–4.")


#                                       Edit Settings Menu

def edit_settings_menu() -> None:
    """Menu for editing settings"""
    while True:
        print("\n--- Edit Settings ---\nSelect from the following menu")
        print("1. Change Root Path")
        print("2. Toggle Case Sensitivity")
        print("3. Change Display Size")
        print("4. Back to Main Menu")

        choice = safe_input("Choose an option: ")
        if choice == "QUIT_SIGNAL":
            return

        try:
            choice = int(choice)
        except ValueError:
            print("⚠️ Invalid menu choice! Please enter a number 1–4.")
            continue

        if choice == 1:  # Change root path
            print(f"\nCurrent Root Path: {config['root_path']}")
            while True:
                new_path = safe_input("Enter new root path: ")
                if new_path == "QUIT_SIGNAL":
                    break
                from pathlib import Path
                path = Path(new_path) 
                if path.exists() and path.is_dir():
                    set_root_path(new_path)
                    print(f"\n✔️ Root Path updated successfully!")
                    print(f"   New Root Path: {config['root_path']}")
                    break
                else:
                    print("⚠️ Invalid input! That path does not exist or is not a directory. Try again.")

        elif choice == 2:  # Case sensitivity with yes/no option
            print(f"\nCase Sensitive (current): {config['case_sensitive']}")
            confirm = safe_input("Do you want to change this? (y/n): ")
            if confirm == "QUIT_SIGNAL":
                continue
            if confirm.lower() in ("y", "yes"):
                toggle_case_sensitive()
                print(f"\n✔️ Case Sensitivity updated successfully!")
                print(f"   Case Sensitive (new): {config['case_sensitive']}")
            elif confirm.lower() in ("n", "no"):
                print("\nNo changes made to Case Sensitivity.")
            else:
                print("⚠️ Invalid input! Please type 'y' or 'n'.")

        elif choice == 3:  # Change display size
            print(f"\nCurrent Display Size: {config['display_size']}")
            while True:
                size = safe_input("Enter new display size (3-20): ")
                if size == "QUIT_SIGNAL":
                    break
                try:
                    size = int(size)
                    if 3 <= size <= 20:
                        set_display_size(size)
                        print(f"\n✔️ Display Size updated successfully!")
                        print(f"   New Display Size: {config['display_size']}")
                        break
                    else:
                        print("⚠️ Invalid input! Display size must be between 3 and 20.")
                except ValueError:
                    print("⚠️ Invalid input! Please enter a valid number.")

        elif choice == 4:
            return

        else:
            print("⚠️ Invalid menu choice! Please select 1–4.")


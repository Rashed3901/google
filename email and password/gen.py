#!/usr/bin/env python3

OUTPUT_FILE = "user_ids.txt"

def get_exact_range():
    while True:
        user_input = input("Enter the exact number range (e.g. 1673982-2000993): ").strip()
        if '-' not in user_input:
            print("Please enter a range using '-' (e.g. 1673982-2000993).")
            continue
        start_str, end_str = user_input.split("-", 1)
        try:
            start = int(start_str.strip())
            end = int(end_str.strip())
            if start > end:
                print("Start number must be less than or equal to end number.")
                continue
            return start, end
        except ValueError:
            print("Please enter valid integers.")
            continue

def get_yes_no(prompt):
    while True:
        choice = input(prompt + " [y/n]: ").strip().lower()
        if choice == 'y':
            return True
        elif choice == 'n':
            return False
        else:
            print("Please enter 'y' or 'n'.")

def main():
    wants_exact = get_yes_no("Do you want to enter an exact number range?")
    
    if not wants_exact:
        print("You chose not to enter an exact number range. Exiting...")
        return

    start, end = get_exact_range()
    print(f"Generating IDs from {start} to {end} and saving to '{OUTPUT_FILE}'...")

    try:
        # Open in write mode to overwrite any existing content
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            for num in range(start, end + 1):
                f.write(f"s{num}@edu.moe.om\n")
        print(f"Done! IDs saved to '{OUTPUT_FILE}'.")
    except IOError as e:
        print("Error writing file:", e)

if __name__ == "__main__":
    main()
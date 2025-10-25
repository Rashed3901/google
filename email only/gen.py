#!/usr/bin/env python3

OUTPUT_FILE = "user_id.txt"
MULTIPLIER = 100_000
MIN_LIMIT = 1_000_000
MAX_LIMIT = 10_000_000

def get_range(prompt):
    while True:
        user_input = input(prompt).strip()
        if '-' not in user_input:
            print("Please enter a range using '-' (e.g. 16-24).")
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

    if wants_exact:
        while True:
            start, end = get_range("Enter the exact number range (e.g. 1673982-2000993): ")
            if start < MIN_LIMIT or end < MIN_LIMIT:
                print(f"❌ Both numbers must be at least {MIN_LIMIT:,}. Try again.")
                continue
            if start > MAX_LIMIT or end > MAX_LIMIT:
                print(f"❌ Numbers cannot exceed {MAX_LIMIT:,}. Try again.")
                continue
            break
    else:
        start, end = get_range("Enter the number range (e.g. 16-24): ")
        start *= MULTIPLIER
        end *= MULTIPLIER
        if end > MAX_LIMIT:
            print(f"❌ The multiplied range exceeds {MAX_LIMIT:,}. Try again with smaller numbers.")
            return

    print(f"Generating IDs from {start} to {end} and saving to '{OUTPUT_FILE}'...")

    try:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            for num in range(start, end + 1):
                f.write(f"s{num}@edu.moe.om\n")
        print(f"✅ Done! IDs saved to '{OUTPUT_FILE}'.")
    except IOError as e:
        print("Error writing file:", e)

if __name__ == "__main__":
    main()
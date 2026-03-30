import os
from printAlgResult import (print_hill_climbing_report, print_random_restart_report, export_hill_climbing_report, export_random_restart_report)

def get_valid_input():
    while True:
        user_input = input("Enter the number of queens (default 8): n =").strip()
        
        if user_input == "":
            return 8

        # check for non-integer input
        if not user_input.isdigit():
            print("Error: Input must be a positive integer.")
            continue

        n = int(user_input)

        # condition checks
        if n == 0:
            print("Error: n cannot be 0.")
            continue

        # warning for n < 4 (except n == 1)
        if n < 4 and n != 1:
            print("Warning: This algorithm may not have solutions for n < 4 (except n = 1).")
            choice = input("Do you want to change n? (y/n): ").strip().lower()

            if choice == 'y':
                continue 
            elif choice == 'n':
                return n
            else:
                print("Invalid choice. Please respond with 'y' or 'n'.")
                continue

        return n

def main():
    n = get_valid_input()

    print_hill_climbing_report(n, sw=False)
    print_hill_climbing_report(n, sw=True)
    print_random_restart_report(n)

    out_dir = os.path.join("output", f"n={n}")
    os.makedirs(out_dir, exist_ok=True)

    f1 = f"{n}queens_hc_ns.md"
    f2 = f"{n}queens_hc_s.md"
    f3 = f"{n}queens_rr.md"
    export_hill_climbing_report(n, os.path.join(out_dir, f1), sw=False)
    export_hill_climbing_report(n, os.path.join(out_dir, f2), sw=True)
    export_random_restart_report(n, os.path.join(out_dir, f3))
    
    print(f"\nExported results with visuals across steps in output folder: {f1}, {f2}, {f3}")

if __name__ == "__main__":
    main()

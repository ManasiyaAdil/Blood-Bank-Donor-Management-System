import json
import os
import sys

# Global donor list and file
donor_list = []
file_name = "donor_data.txt"

# Load donor data from file
def load_donors():
    if os.path.exists(file_name):
        with open(file_name, "r") as file:
            try:
                return json.load(file)
            except:
                return []
    return []

# Save donor data to file
def save_donors():
    with open(file_name, "w") as file:
        json.dump(donor_list, file)

# Generate unique donor ID (always increasing)
def get_new_id():
    if not donor_list:
        return "1001"
    else:
        max_id = max(int(d["DonorID"]) for d in donor_list)
        return str(max_id + 1)

# Check if blood group is valid
def valid_blood_group(bg):
    groups = ['A+', 'A-', 'B+', 'B-', 'O+', 'O-', 'AB+', 'AB-']
    return bg.upper() in groups

# Add new donor
def register_donor():
    name = input("Enter full name: ").strip()
    age_input = input("Enter age: ").strip()
    phone = input("Enter contact number (10 digits): ").strip()
    group = input("Enter blood group: ").strip().upper()

    if not age_input.isdigit() or not (18 <= int(age_input) <= 65):
        print("Invalid age. Age must be between 18 and 65.\n")
        return
    if not (phone.isdigit() and len(phone) == 10):
        print("Invalid phone number. Must be 10 digits.\n")
        return
    if not valid_blood_group(group):
        print("Invalid blood group.\n")
        return

    new_donor = {
        "DonorID": get_new_id(),
        "Name": name,
        "Age": int(age_input),
        "Contact": phone,
        "BloodGroup": group
    }

    donor_list.append(new_donor)
    save_donors()
    print("Donor added to database.\n")

# Show all donor records
def view_all_donors():
    if not donor_list:
        print("No donors available.\n")
        return

    print("\n--- Donor Records ---")
    for donor in donor_list:
        print(f"ID: {donor['DonorID']} | Name: {donor['Name']} | Age: {donor['Age']} | Blood Group: {donor['BloodGroup']} | Phone: {donor['Contact']}")
    print()

# Find donor by blood group
def find_by_blood_group():
    bg = input("Enter blood group to search: ").strip().upper()
    matched = [d for d in donor_list if d["BloodGroup"] == bg]

    if matched:
        print(f"\nMatched donors for group {bg}:")
        for d in matched:
            print(f"- {d['Name']}, Contact: {d['Contact']}")
    else:
        print("No matching donors found.\n")

# Modify donor info
def modify_donor():
    did = input("Enter donor ID to update: ").strip()
    for d in donor_list:
        if d["DonorID"] == did:
            print(f"Updating donor: {d['Name']}")
            d["Name"] = input("New Name (or press Enter to keep same): ") or d["Name"]

            new_age = input("New Age (18–65) (or Enter to keep same): ")
            if new_age.isdigit() and 18 <= int(new_age) <= 65:
                d["Age"] = int(new_age)

            new_phone = input("New Contact (10 digits or Enter): ").strip()
            if new_phone.isdigit() and len(new_phone) == 10:
                d["Contact"] = new_phone

            new_bg = input("New Blood Group (or press Enter): ").upper()
            if new_bg and valid_blood_group(new_bg):
                d["BloodGroup"] = new_bg

            save_donors()
            print("Donor info updated.\n")
            return

    print("Donor ID not found.\n")

# Delete donor by ID
def remove_donor():
    did = input("Enter donor ID to delete: ").strip()
    global donor_list
    updated_list = [d for d in donor_list if d["DonorID"] != did]

    if len(updated_list) != len(donor_list):
        donor_list = updated_list
        save_donors()
        print("Donor removed.\n")
    else:
        print("Donor ID not found.\n")

# Show blood group summary
def group_summary():
    summary = {}
    for d in donor_list:
        group = d["BloodGroup"]
        summary[group] = summary.get(group, 0) + 1

    print("\nBlood Group Summary:")
    for g, count in summary.items():
        print(f"{g}: {count} donor(s)")
    print()

# Main CLI menu
def menu():
    global donor_list
    donor_list = load_donors()

    while True:
        print("\n=== BLOOD BANK DONOR MANAGEMENT ===")
        print("1. Register Donor")
        print("2. View Donors")
        print("3. Search by Blood Group")
        print("4. Update Donor")
        print("5. Delete Donor")
        print("6. Blood Group Stats")
        print("7. Exit")

        choice = input("Select an option (1-7): ").strip()

        if choice == '1':
            register_donor()
        elif choice == '2':
            view_all_donors()
        elif choice == '3':
            find_by_blood_group()
        elif choice == '4':
            modify_donor()
        elif choice == '5':
            remove_donor()
        elif choice == '6':
            group_summary()
        elif choice == '7':
            print("Exiting program. Thank you!")
            sys.exit()
        else:
            print("Invalid input. Please select between 1–7.\n")

if __name__ == "__main__":
    menu()

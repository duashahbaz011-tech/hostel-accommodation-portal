# Hostel Accommodation Portal - Assignment 3
# Team: 25L-5223 and 25L-5215

import csv

ROOMS_FILE = "rooms.csv"
STUDENTS_FILE = "students.csv"

# username and password of the warden accounts
USERS = {"admin": "admin123", "warden": "hostel1"}

def load_file(filename):
    """Read a csv file and return all rows as a list."""
    data = []
    try:
        file = open(filename, "r")
        reader = csv.reader(file)
        for row in reader:
            data.append(row)
        file.close()
    except FileNotFoundError:
        print(filename, "not found. Starting with an empty list.")
    except PermissionError:
        print("Cannot open", filename, "- permission denied.")
    return data


def save_file(filename, data):
    """Write a list of rows to a csv file."""
    file = None
    try:
        file = open(filename, "w", newline="")
        writer = csv.writer(file)
        writer.writerows(data)
    except PermissionError:
        print("Cannot save", filename, "- permission denied.")
    finally:
        if file:
            file.close()

def user_login(username, password):
    """Return True if username and password are correct, otherwise False."""
    if username in USERS and USERS[username] == password:
        return True
    return False

def add_room(rooms, room_no, capacity, rent):
    """Add a new room. Returns a message."""
    room_no = room_no.strip().upper()
    if room_no == "":
        return "Room number cannot be empty."
    for room in rooms:
        if room[0] == room_no:
            return "Room already exists."
    try:
        capacity = int(capacity)
        rent = int(rent)
    except ValueError:
        return "Capacity and rent must be numbers."
    if capacity <= 0 or rent < 0:
        return "Capacity must be above 0 and rent cannot be negative."
    rooms.append([room_no, str(capacity), "0", str(rent)])
    return "Room " + room_no + " added."


def add_student(students, roll_no, name):
    """Add a new student with no room. Returns a message."""
    roll_no = roll_no.strip().upper()
    name = name.strip()
    if roll_no == "" or name == "":
        return "Roll number and name cannot be empty."
    for student in students:
        if student[0] == roll_no:
            return "This roll number is already registered."
    students.append([roll_no, name, ""])
    return "Student " + name + " added."

def search_record(records, keyword):
    """Return all rows that contain the keyword anywhere."""
    found = []
    for row in records:
        for item in row:
            if keyword.lower() in item.lower():
                found.append(row)
                break
    return found


def show_records(records, heading):
    """Print rows one by one."""
    print(heading)
    if len(records) == 0:
        print("  No records.")
    for row in records:
        print("  ", " | ".join(row))

def allocate_room(students, rooms, roll_no, room_no):
    """Give a room to a student. Returns a message."""
    roll_no = roll_no.strip().upper()
    room_no = room_no.strip().upper()

    student = None
    for s in students:
        if s[0] == roll_no:
            student = s
    room = None
    for r in rooms:
        if r[0] == room_no:
            room = r

    if student is None:
        return "Student not found."
    if room is None:
        return "Room not found."
    if student[2] != "":
        return "Student already has room " + student[2] + "."
    if int(room[2]) >= int(room[1]):
        return "Room " + room_no + " is full."

    room[2] = str(int(room[2]) + 1)
    student[2] = room_no
    return student[1] + " got room " + room_no + "."


def vacate_room(students, rooms, roll_no):
    """Take a student out of their room. Returns a message."""
    roll_no = roll_no.strip().upper()
    for s in students:
        if s[0] == roll_no:
            if s[2] == "":
                return "This student has no room."
            for r in rooms:
                if r[0] == s[2]:
                    r[2] = str(int(r[2]) - 1)
            old_room = s[2]
            s[2] = ""
            return s[1] + " left room " + old_room + "."
    return "Student not found."

def generate_report(students, rooms):
    """Print a hostel summary and return the number of occupied beds."""
    total_beds = 0
    occupied = 0
    for room in rooms:
        total_beds = total_beds + int(room[1])
        occupied = occupied + int(room[2])

    without_room = 0
    for student in students:
        if student[2] == "":
            without_room = without_room + 1

    print("----- HOSTEL REPORT -----")
    print("Total rooms:", len(rooms))
    print("Total students:", len(students))
    print("Total beds:", total_beds)
    print("Occupied beds:", occupied)
    print("Free beds:", total_beds - occupied)
    if total_beds > 0:
        print("Occupancy:", round(occupied * 100 / total_beds, 1), "%")
    print("Students without a room:", without_room)
    return occupied

def main():
    print("=== HOSTEL ACCOMMODATION PORTAL ===")
    rooms = load_file(ROOMS_FILE)
    students = load_file(STUDENTS_FILE)

    # login with 3 tries
    tries = 0
    logged_in = False
    while tries < 3:
        username = input("Username: ")
        password = input("Password: ")
        if user_login(username, password):
            logged_in = True
            break
        print("Wrong username or password.")
        tries = tries + 1
    if not logged_in:
        print("Too many wrong attempts. Bye.")
        return

    print("Login successful.")
    while True:
        print()
        print("1. Add room")
        print("2. Add student")
        print("3. Search student")
        print("4. View rooms")
        print("5. View students")
        print("6. Allocate room")
        print("7. Vacate room")
        print("8. Report")
        print("0. Exit")
        choice = input("Enter choice: ")

        if choice == "1":
            room_no = input("Room no: ")
            capacity = input("Capacity: ")
            rent = input("Rent: ")
            print(add_room(rooms, room_no, capacity, rent))
            save_file(ROOMS_FILE, rooms)
        elif choice == "2":
            roll_no = input("Roll no: ")
            name = input("Name: ")
            print(add_student(students, roll_no, name))
            save_file(STUDENTS_FILE, students)
        elif choice == "3":
            keyword = input("Search for: ")
            show_records(search_record(students, keyword), "Search results (roll no | name | room):")
        elif choice == "4":
            show_records(rooms, "Rooms (room no | capacity | occupied | rent):")
        elif choice == "5":
            show_records(students, "Students (roll no | name | room):")
        elif choice == "6":
            roll_no = input("Student roll no: ")
            room_no = input("Room no: ")
            print(allocate_room(students, rooms, roll_no, room_no))
            save_file(ROOMS_FILE, rooms)
            save_file(STUDENTS_FILE, students)
        elif choice == "7":
            roll_no = input("Student roll no: ")
            print(vacate_room(students, rooms, roll_no))
            save_file(ROOMS_FILE, rooms)
            save_file(STUDENTS_FILE, students)
        elif choice == "8":
            generate_report(students, rooms)
        elif choice == "0":
            print("Data saved. Goodbye!")
            break
        else:
            print("Invalid choice, please enter a number from the menu.")


main()

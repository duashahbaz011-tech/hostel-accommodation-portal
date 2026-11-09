# Hostel Accommodation Portal

Assignment 3 - End-to-End Portal Design (Python, console based)
Team: 25L-5223 and 25L-5215

## About
A simple hostel management program. The warden logs in and can add rooms and students, search students, allocate or vacate rooms and see a report. Data is stored in CSV files.

## Files
- `Hostel_Portal_Assignment3.ipynb` - notebook with explanation, code and sample runs
- `hostel_portal.py` - the same code as one script
- `rooms.csv` and `students.csv` - created automatically when the program is run

## How to run
```
python hostel_portal.py
```
Login: `admin` / `admin123` (or `warden` / `hostel1`)

## Concepts used
- Functions with parameters and return values: `user_login`, `add_room`, `add_student`, `search_record`, `allocate_room`, `vacate_room`, `generate_report`
- Loops: `while True` menu, `for` loops for searching and report
- File handling: reading and writing CSV files
- Exception handling: `FileNotFoundError`, `PermissionError`, `ValueError` with `try / except / finally`

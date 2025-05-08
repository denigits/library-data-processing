import csv
import sys
from datetime import datetime

# Read book data from a CSV file
def read_books(file_path):
    books = []
    try:
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            expected_columns = {'Title', 'Author', 'Year', 'Status', 'DueDate'}
            if not expected_columns.issubset(reader.fieldnames):
                print("Error: Input CSV is missing one or more required columns.")
                sys.exit(1)

            for row in reader:
                try:
                    row['Year'] = int(row['Year'])
                    books.append(row)
                except ValueError:
                    print(f"Warning: Invalid year format for book '{row.get('Title', 'Unknown')}', skipping entry.")
        
        if not books:
            print("Warning: No valid book entries found in the file.")

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred while reading the file: {e}")
        sys.exit(1)

    return books

# Count books by availability status
def count_status(books):
    available = sum(1 for book in books if book['Status'].strip().lower() == 'available')
    borrowed = sum(1 for book in books if book['Status'].strip().lower() == 'borrowed')
    return available, borrowed

# Find the oldest and newest books
def find_oldest_and_newest(books):
    sorted_books = sorted(books, key=lambda b: b['Year'])
    return sorted_books[0], sorted_books[-1]

# Identify books that are overdue
def find_overdue_books(books):
    today = datetime.today().date()
    overdue = []
    for book in books:
        if book['Status'].strip().lower() == 'borrowed' and book['DueDate']:
            try:
                due_date = datetime.strptime(book['DueDate'], '%d-%m-%Y').date()
                if due_date < today:
                    overdue.append(book)
            except ValueError:
                print(f"Warning: Invalid date format for '{book['Title']}', skipping due date check.")
    return overdue

# Write summary report to output file
def write_summary(output_path, available, borrowed, oldest, newest, overdue):
    try:
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write("Library Summary Report\n")
            file.write("=======================\n")
            file.write(f"Available Books: {available}\n")
            file.write(f"Borrowed Books: {borrowed}\n\n")
            file.write(f"Oldest Book: {oldest['Title']} ({oldest['Year']}) by {oldest['Author']}\n")
            file.write(f"Newest Book: {newest['Title']} ({newest['Year']}) by {newest['Author']}\n\n")
            file.write("Overdue Books:\n")
            if overdue:
                for book in overdue:
                    file.write(f"- {book['Title']} by {book['Author']} (Due: {book['DueDate']})\n")
            else:
                file.write("None\n")
    except IOError as e:
        print(f"Error: Unable to write to output file: {e}")

# Main program entry point
def main():
    if len(sys.argv) != 2:
        print("Usage: python library_stats.py books.csv")
        sys.exit(1)

    input_file = sys.argv[1]
    books = read_books(input_file)

    if not books:
        print("No valid data to process. Exiting.")
        sys.exit(1)

    available, borrowed = count_status(books)
    oldest, newest = find_oldest_and_newest(books)
    overdue = find_overdue_books(books)

    output_file = "library_summary.txt"
    write_summary(output_file, available, borrowed, oldest, newest, overdue)
    print(f"Report generated: {output_file}")

if __name__ == "__main__":
    main()

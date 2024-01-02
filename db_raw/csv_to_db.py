import csv
import sqlite3

# File paths
csv_file = './output.csv'
sqlite_db = './database.db'

# Connect to the SQLite database (this will create the database if it doesn't exist)
conn = sqlite3.connect(sqlite_db)
cursor = conn.cursor()

# Create a table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        FIO TEXT,
        DOB TEXT,
        Position TEXT,
        Unit TEXT,
        Passport TEXT,
        Passport_Issue_Date TEXT,
        Issued_By TEXT,
        Taxpayer_Number TEXT,
        Social_Security_Number TEXT,
        Address TEXT,
        Phone_Number TEXT,
        Social_Media TEXT,
        Email TEXT,
        Status TEXT,
        Verified TEXT,
        Source TEXT,
        Image_File TEXT
    )
''')

# Read the CSV file and insert data into the SQLite database
with open(csv_file, 'r', encoding='utf-8') as file:
    csv_reader = csv.reader(file)
    header = next(csv_reader)  # Skip header
    for row in sorted(csv_reader, key=lambda x: x[0]):  # Sort by the first column (FIO)        # Insert data, omitting the 'id' and 'created' fields as they are auto-populated
        cursor.execute('INSERT INTO posts (FIO, DOB, Position, Unit, Passport, Passport_Issue_Date, Issued_By, Taxpayer_Number, Social_Security_Number, Address, Phone_Number, Social_Media, Email, Status, Verified, Source, Image_File) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', row)

# Commit the changes and close the connection
conn.commit()
conn.close()
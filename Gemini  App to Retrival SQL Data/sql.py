import sqlite3

# Connect to sqlite
Connection = sqlite3.connect("student.db")

# Create a cursor object to insert record, create table, retrieve
cursor = Connection.cursor()

# Create the table
table_info = """
CREATE TABLE IF NOT EXISTS STUDENT(
    NAME VARCHAR(25),
    CLASS VARCHAR(25),
    SECTION VARCHAR(25),
    MARKS INT
);
"""
cursor.execute(table_info)  # Create table if it doesn't exist

# Insert records into the STUDENT table
cursor.execute('''Insert Into STUDENT values('Krish', 'Data Science', 'A', 90)''')
cursor.execute('''Insert Into STUDENT values('Tanmay', 'Data Science', 'B', 100)''')
cursor.execute('''Insert Into STUDENT values('Dhanush', 'Data Science', 'A', 89)''')
cursor.execute('''Insert Into STUDENT values('Shivam', 'Data Science', 'A', 78)''')
cursor.execute('''Insert Into STUDENT values('Tommy', 'Data Science', 'C', 56)''')

# Commit the changes to the database
Connection.commit()

# Display all the records
print("The inserted records are:")

data = cursor.execute('''SELECT * FROM STUDENT''')

for row in data:
    print(row)

# Close the connection
Connection.close()

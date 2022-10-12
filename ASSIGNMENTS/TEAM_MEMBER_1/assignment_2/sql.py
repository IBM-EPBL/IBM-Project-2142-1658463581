import sqlite3

conn = sqlite3.connect('students.db')
print('opened database successfully')

conn.execute('CREATE TABLE students (name TEXT, email TEXT, mobile TEXT, city TEXT, state TEXT, country TEXT, password TEXT)')
print("Table created successfully")
conn.close()  

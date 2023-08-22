import sqlite3

# Connect to the database
connection = sqlite3.connect('db.sqlite3')

cursor = connection.cursor()

# Execute the query
query = "SELECT * FROM Data;"
cursor.execute(query)

# Fetch and display the results
rows = cursor.fetchall()
for row in rows:
    print(row)

connection.close()

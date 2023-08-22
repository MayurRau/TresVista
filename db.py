from modelfile import model
import sqlite3


# Define the database file name
db_file = "tresvista_db.sqlite3"

# Define the table schema
table_schema = """
CREATE TABLE IF NOT EXISTS Data (
    id INTEGER PRIMARY KEY,
    Category TEXT,
    Line_Item TEXT,
    Year TEXT,
    Period TEXT,
    Estimate_Actual TEXT,
    Value REAL
);
"""


def store_data_in_database(dataframe, connect):
    cursor = connect.cursor()

    for index, row in dataframe.iterrows():
        query = "INSERT INTO Data (Category, Line_Item, Year, Period, Estimate_Actual, Value) VALUES (?, ?, ?, ?, ?, ?)"
        values = (
            row['Category'],
            row['Line Item'],
            row['Year'],
            row['Period'],
            row['Estimate/Actual'],
            row['Value']
        )
        cursor.execute(query, values)

    connect.commit()


if __name__ == "__main__":
    # Connect to the SQLite database
    connection = sqlite3.connect(db_file)

    # Create the table if it doesn't exist
    with connection:
        connection.execute(table_schema)

    # Get the data using the model function
    data = model()

    # Store the data in the database
    store_data_in_database(data, connection)

    # Close the database connection
    connection.close()

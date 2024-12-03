import sqlite3

# Connect to the SQLite database (it will create the database if it doesn't exist)
conn = sqlite3.connect('users.db')

# Create a cursor object to interact with the database
cursor = conn.cursor()

# Create users table
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE  -- Added email field for user registration
)
''')

# Create plans table
cursor.execute('''
CREATE TABLE IF NOT EXISTS plans (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,  -- Updated to 'name' instead of 'plan_name'
    duration TEXT NOT NULL,
    price REAL NOT NULL
)
''')

# Create members table
cursor.execute('''
CREATE TABLE IF NOT EXISTS members (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    surname TEXT NOT NULL,
    age INTEGER NOT NULL,
    address TEXT NOT NULL,
    mobile TEXT NOT NULL,
    email TEXT NOT NULL,  -- Email field added for members
    plan_id INTEGER,
    payment_method TEXT NOT NULL,
    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (plan_id) REFERENCES plans (id)
)
''')

# Create coaches table
cursor.execute('''
CREATE TABLE IF NOT EXISTS coaches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER NOT NULL,
    experience TEXT NOT NULL,
    email TEXT NOT NULL,
    mobile TEXT NOT NULL
)
''')

# Create equipments table
cursor.execute('''
CREATE TABLE IF NOT EXISTS equipments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    quantity INTEGER NOT NULL
)
''')

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Database and tables created successfully!")

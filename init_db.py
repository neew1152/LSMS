import sqlite3

# Connect to database (this creates a file named library.db in your folder)
conn = sqlite3.connect('library.db')
cursor = conn.cursor()

# 1. Create Users Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    role TEXT NOT NULL,
    pin TEXT NOT NULL
)
''')

# 2. Create Books Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS books (
    book_id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    status TEXT DEFAULT 'Available'
)
''')

# 3. Create Logs Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS logs (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT,
    book_id TEXT,
    action TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
''')

# Add some test data (Ignore errors if they already exist)
try:
    # Test Student: ID 'S01', PIN '1234'
    cursor.execute("INSERT INTO users (id, name, role, pin) VALUES ('S01', 'Alice', 'student', '1234')")
    # Test Teacher: ID 'T01', PIN '0000'
    cursor.execute("INSERT INTO users (id, name, role, pin) VALUES ('T01', 'Mrs. Smith', 'teacher', '0000')")
    # Test Book: ID 'B01'
    cursor.execute("INSERT INTO books (book_id, title, status) VALUES ('B01', 'The Little Prince', 'Available')")
    print("Database created and test data added!")
except sqlite3.IntegrityError:
    print("Database already exists with test data.")

conn.commit()
conn.close()
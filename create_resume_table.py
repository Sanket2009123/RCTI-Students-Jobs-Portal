import sqlite3

conn = sqlite3.connect("database/database.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS resumes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,

    full_name TEXT,
    email TEXT,
    phone TEXT,
    address TEXT,

    objective TEXT,

    education TEXT,
    skills TEXT,
    experience TEXT,
    projects TEXT,
    certificates TEXT,
    languages TEXT,
    achievements TEXT,
    hobbies TEXT,

    photo TEXT,

    template_name TEXT DEFAULT 'modern',
    theme_color TEXT DEFAULT 'blue',

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY(student_id) REFERENCES students(id)
);
""")

conn.commit()
conn.close()

print("Resume table created successfully.")
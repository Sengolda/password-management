import sqlite3

conn  = sqlite3.connect('passwords.db')
conn.execute("""CREATE TABLE IF NOT EXISTS users(
        "user_name"    TEXT NOT NULL,
        "master_password"    TEXT NOT NULL,
        "passwords" TEXT[],
        PRIMARY KEY("user_name")
)""")

import sqlite3

connection = sqlite3.connect('kudos.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO users (username, full_name, is_admin) VALUES (?, ?, ?)",
            ('alice', 'Alice Smith', 0))
cur.execute("INSERT INTO users (username, full_name, is_admin) VALUES (?, ?, ?)",
            ('bob', 'Bob Jones', 0))
cur.execute("INSERT INTO users (username, full_name, is_admin) VALUES (?, ?, ?)",
            ('admin', 'Admin User', 1))

cur.execute("INSERT INTO kudos (sender_id, receiver_id, message, is_visible) VALUES (?, ?, ?, ?)",
            (1, 2, 'Thanks for helping with the report!', 1))
cur.execute("INSERT INTO kudos (sender_id, receiver_id, message, is_visible) VALUES (?, ?, ?, ?)",
            (2, 1, 'Great presentation today.', 1))
cur.execute("INSERT INTO kudos (sender_id, receiver_id, message, is_visible) VALUES (?, ?, ?, ?)",
            (1, 2, 'This message should be hidden.', 0))

connection.commit()
connection.close()

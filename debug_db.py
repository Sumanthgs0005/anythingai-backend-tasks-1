import sqlite3
conn = sqlite3.connect('tasks.db')
c = conn.cursor()
try:
    for row in c.execute('SELECT id, email, hashed_password, is_admin FROM users'):
        print(row)
except Exception as e:
    print('ERROR', e)
finally:
    conn.close()

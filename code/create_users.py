import sqlite3

connection = sqlite3.connect('data.db')

cursor = connection.cursor()

user = [1, 'bogosi', 'chance']
insert_query = "INSERT INTO users VALUES (?, ?, ?)"
cursor.execute(insert_query, user)

users = [
    (2, 'nthabi', 'infinity'),
    (3, 'david', 'dev')
]
cursor.executemany(insert_query, users)

select_query = "SELECT * FROM users"
for row in cursor.execute(select_query):
    print(row)


connection.commit()
connection.close()

import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO posts (title, content, image) VALUES (?, ?, ?)",
            ('Лопин Александр Сергеевич', 'Командир батальона,  подполковник', 'Abakov.jpg')
            )

cur.execute("INSERT INTO posts (title, content, image) VALUES (?, ?, ?)",
            ('Шурасьев Николай Константинович', 'Заместитель командира батальона, капитан', 'Aduev.jpg')
            )

connection.commit()
connection.close()

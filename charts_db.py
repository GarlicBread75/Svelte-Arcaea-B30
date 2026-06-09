import sqlite3 as sql


def csv_to_db():
    global charts_db

    cursor = charts_db.cursor()
    cursor.execute('SELECT COUNT(*) FROM charts;')
    count = cursor.fetchone()[0]

    if count < 1:
        with open('charts.csv', 'r') as file:
            for line in file:
                data = line.strip().split(',')
                charts_db.execute(f"INSERT INTO charts (title, difficulty, constant, score) VALUES (\"{data[0]}\", \"{data[1]}\", {float(data[2])}, {int(data[3])});")
            charts_db.commit()

def create_charts_table():
    global charts_db

    charts_db.execute('''CREATE TABLE IF NOT EXISTS charts (id INTEGER PRIMARY KEY,
                                                            title TEXT,
                                                            difficulty TEXT,
                                                            constant REAL,
                                                            score INTEGER);''')

def create_users_table():
    global users_db

    users_db.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY,
                                                          username TEXT,
                                                          password TEXT,
                                                          role TEXT DEFAULT 'user');''')

def print_db(cursor):
    cursor.execute('SELECT * FROM charts;')
    for row in cursor.fetchall():
        print(row)


if __name__ == "__main__":
    charts_db = sql.connect('charts_db')
    users_db = sql.connect('users.db')
    
    create_charts_table()
    create_users_table()
    csv_to_db()
    
    charts_db.close()
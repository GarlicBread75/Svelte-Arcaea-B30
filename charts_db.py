import sqlite3 as sql


def csv_to_db():
    global db

    with open('charts.csv', 'r') as file:
        for line in file:
            data = line.strip().split(',')
            db.execute(f"INSERT INTO charts (title, difficulty, constant, score) VALUES (\"{data[0]}\", \"{data[1]}\", {float(data[2])}, {int(data[3])});")
        db.commit()

def create_table():
    global db

    db.execute("DROP TABLE IF EXISTS charts")
    db.execute('''CREATE TABLE charts(id INTEGER PRIMARY KEY,
                                      title TEXT,
                                      difficulty TEXT,
                                      constant REAL,
                                      score INTEGER);''')

def print_db():
    global cursor

    cursor.execute('SELECT * FROM charts;')
    for row in cursor.fetchall():
        print(row)

if __name__ == "__main__":
    db = sql.connect('charts.db')
    cursor = db.cursor()
    
    create_table()
    csv_to_db()
    #print_db()
    
    db.close()
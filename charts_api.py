from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request
from fastapi.responses import Response
import sqlite3 as sql
import json


app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins = ['*'], allow_credentials = True, allow_methods = ['*'], allow_headers = ['*'])


@app.get('/charts')
def get_charts():
    charts_db = sql.connect('charts.db')
    charts_db.row_factory = sql.Row
    cursor = charts_db.cursor()
    cursor.execute('SELECT id, title, difficulty, constant, score FROM charts ORDER BY score')
    rows = cursor.fetchall()
    charts_db.close()

    return [dict(row) for row in rows]

@app.get('/b30')
def get_b30():
    charts_db = sql.connect('charts.db')
    charts_db.row_factory = sql.Row
    cursor = charts_db.cursor()
    cursor.execute('SELECT id, title, difficulty, constant, score FROM charts ORDER BY score DESC LIMIT 30')
    rows = cursor.fetchall()
    charts_db.close()

    return [dict(row) for row in rows]

@app.post('/update_score')
def update_score(data: dict):
    charts_db = sql.connect('charts.db')

    charts_db.execute(f"UPDATE charts SET score = {data['score']} WHERE id = {data['id']}")

    charts_db.commit()
    charts_db.close()

    return {"success": True}

@app.post('/add_chart')
def add_chart(data: dict):
    charts_db = sql.connect('charts.db')

    charts_db.execute(f"INSERT INTO charts (title, difficulty, constant, score) VALUES (\"{data[0]}\", \"{data[1]}\", {float(data[2])}, {int(data[3])});")

    charts_db.commit()
    charts_db.close()

    return {"success": True}

@app.post('/delete_chart')
def delete_chart(data: dict):
    chart_id = data.get('id')

    if chart_id is None:
        return {"success": False}

    charts_db = sql.connect('charts.db')
    charts_db.execute(f"DELETE FROM CHARTS WHERE id = {chart_id}")
    charts_db.commit()
    charts_db.close()

    return {"success": True}

@app.post('/login')
def login(data: dict):
    users_db = sql.connect('users.db')
    users_db.row_factory = sql.Row
    cursor = users_db.cursor()

    cursor.execute(f"SELECT username, role FROM users WHERE username = \"{data['username']}\" AND password = \"{data['password']}\"")
    result = cursor.fetchone()
    users_db.close()

    if result is None:
        return {"success": False, "message":"User Doesn't Exist!"}
    return {"success": True, "username": result['username'], "role": result['role']}

@app.post('/signup')
def signup(data: dict):
    users_db = sql.connect('users.db')
    users_db.row_factory = sql.Row
    cursor = users_db.cursor()

    cursor.execute(f"SELECT id FROM users WHERE username = \"{data['username']}\"")
    if cursor.fetchone() is not None:
        users_db.close()
        return {"success": False, "message": "User Already Exists!"}

    cursor.execute(f"INSERT INTO users (username, password, role) VALUES (\"{data['username']}\", \"{data['password']}\", \"user\");")
    users_db.commit()
    users_db.close()
    return {"success":True}

@app.exception_handler(404)
async def custom_404(request: Request, exc):
    data = {'         _____                                   _____     ':0,  
            '        /    /                                  /    /     ':0,
            '       /    /                                  /    /      ':0,
            '      /    /                                  /    /       ':0,
            '     /    /             .-\'\'` \'\'-.           /    /        ':0,
            '    /    /  ___        .\'          \'.       /    /  ___     ':0,
            '   /    /  |   |      /              `     /    /  |   |    ':0,
            '  /    \'   |   |     \'                \'   /    \'   |   |    ':0,
            ' /    \'----|   |---. |         .-.    |  /    \'----|   |---.':0,
            '/          |   |   | .        |   |   . /          |   |   |':0,
            '\'----------|   |---\'  .       \'._.\'  /  \'----------|   |---\'':0,
            '           |   |       \'._         .\'              |   |    ':0,
            '          /____\         \'-....-\'`               /____\ ':0}
    return Response(content = json.dumps(data, indent = 4), media_type = 'application/json')    
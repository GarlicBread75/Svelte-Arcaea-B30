from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
import sqlite3 as sql


app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins = ['*'], allow_credentials = True, allow_methods = ['*'], allow_headers = ['*'])


@app.get('/charts')
def get_charts():
    db = sql.connect('charts.db')
    db.row_factory = sql.Row
    cursor = db.cursor()
    cursor.execute('SELECT id, title, difficulty, constant, score FROM charts ORDER BY score')
    rows = cursor.fetchall()
    db.close()

    return [dict(row) for row in rows]

@app.get('/b30')
def get_b30():
    db = sql.connect('charts.db')
    db.row_factory = sql.Row
    cursor = db.cursor()
    cursor.execute('SELECT id, title, difficulty, constant, score FROM charts ORDER BY score DESC LIMIT 30')
    rows = cursor.fetchall()
    db.close()

    return [dict(row) for row in rows]

@app.post('/update_score')
def update_score(data: dict):
    db = sql.connect('charts.db')

    db.execute(f"UPDATE charts SET score = {data['score']} WHERE id = {data['id']}")

    db.commit()
    db.close()

    return {"success": True}
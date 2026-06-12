import psycopg2
import hashlib
from fastapi import FastAPI, Form

app = FastAPI()
@app.post("/register")
def web_register(username: str=Form(...), password: str=Form(...)):
    password = hashlib.sha256(password.encode()).hexdigest()
    conn = psycopg2.connect(
        host="127.0.0.1",
        database="postgres", 
        user="postgres",
        password="1234",
        port="5432"
    )
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM game_users WHERE username = %s", (username,))
    users_exists = cursor.fetchone()
    if users_exists:
       cursor.close()
       conn.close()
       return{"eror": "Этот ID уже существует, выберите другой ID"} 
    else:
        sql_insert ="INSERT INTO game_users (username, password_hash) VALUES(%s,%s)"
        cursor.execute(sql_insert, (username, password))
        conn.commit()
        cursor.close()
        conn.close()
        return{"result":"Регистрация прошла успешно!"}
@app.post("/login")
def web_login(username: str=Form(...), password: str=Form(...)):
    password_hash=hashlib.sha256(password.encode()).hexdigest()
    conn = psycopg2.connect(
        host="127.0.0.1",
        database="postgres", 
        user="postgres",
        password="1234",
        port="5432"
    )
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM game_users WHERE username = %s", (username,))
    user_data=cursor.fetchone()
    if user_data and password_hash == user_data[2]:
        cursor.close()
        conn.close()
        return{"result": "Вход успешно выполнен!"}
    else:
        cursor.close()
        conn.close()
        return{"error": "Неверное имя пользователя или пароль"}
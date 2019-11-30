#!/usr/bin/python3
from bottle import route, run, get, post, request
import psycopg2
import json
import os
import random
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT 

# Connection to Postgresql in Heroku:
URL = 'postgres://ybgqdfwrfktliz:ed949a4fa7a88c55fc89844f3376c3aa59c4d64bde80a54b78b45d8397591960@ec2-46-137-113-157.eu-west-1.compute.amazonaws.com:5432/dckopqv6o4em74'
conn = psycopg2.connect(URL, sslmode='require')
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cur = conn.cursor()

@get("/")
def index():
    return {
        "nombre": random.choice(["Pepe", "Juan", "Fran", "Luis"])
    }

@get("/<table>")
def demo2(table):
    if table == "users":
        query = """SELECT * FROM users;"""
        cur.execute(query)
        result = cur.fetchall()
        return json.dumps(result)
    elif table == "messages":
        query = """SELECT * FROM messages;"""
        cur.execute(query)
        result = cur.fetchall()
        return json.dumps(result)
    elif table == "chats":
        query = """SELECT * FROM chats;"""
        cur.execute(query)
        result = cur.fetchall()
        return json.dumps(result)
    elif table == "iduser":
        query = """select iduser from users order by iduser desc limit 1;"""
        cur.execute(query)
        result = cur.fetchall()
        print(int(result[0][0])+1)
        return json.dumps(result)       

@post('/addUser')
def add():
    name = str(request.forms.get("name"))
    print(name)
    query = """select iduser from users order by iduser desc limit 1;"""
    cur.execute(query)
    result = cur.fetchall()
    iduser = int(result[0][0]) + 1
    query = """INSERT INTO users (iduser, username) VALUES ({}, '{}') RETURNING {};""".format(iduser, name, 'users.iduser')
    cur.execute(query)
    id = cur.fetchone()[0]
    print(id)
    return json.dumps(id)

port = int(os.getenv("PORT", 8080))
print(f"Running server {port}....")

run(host="0.0.0.0", port=port, debug=True)


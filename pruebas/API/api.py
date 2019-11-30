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

@get("/<tabla>")
def demo2(tabla):
    if tabla == "users":
        query = """SELECT * FROM users;"""
        cur.execute(query)
        result = cur.fetchall()
        return json.dumps(result)
    elif tabla == "messages":
        query = """SELECT * FROM messages;"""
        cur.execute(query)
        result = cur.fetchall()
        return json.dumps(result)
    elif tabla == "chats":
        query = """SELECT * FROM chats;"""
        cur.execute(query)
        result = cur.fetchall()
        return json.dumps(result)

# @post('/add')
# def add():
#     print(dict(request.forms))
#     autor=request.forms.get("autor")
#     chiste=request.forms.get("chiste")  
#     return {
#         "inserted_doc": str(coll.addChiste(autor,chiste))}

port = int(os.getenv("PORT", 8080))
print(f"Running server {port}....")

run(host="0.0.0.0", port=port, debug=True)


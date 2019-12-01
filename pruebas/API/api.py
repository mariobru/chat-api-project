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
        "chatAPI": random.choice(["Create users!", "Add Messages"])
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

@get("/chat/<chat_id>/list")
def chatMessages(chat_id):
    chatid = int(chat_id)
    query = """SELECT text FROM messages WHERE chats_idchat={};""".format(chatid)
    cur.execute(query)
    result = cur.fetchall()
    return json.dumps(result)

@get("/user/<user_id>/listmessages")
def userMessages(user_id):
    query = """SELECT text FROM messages WHERE users_iduser={};""".format(user_id)
    cur.execute(query)
    result = cur.fetchall()
    return json.dumps(result)

@post('/user/create')
def createUser():
    name = str(request.forms.get("name"))
    print(name)
    query = """SELECT iduser FROM users ORDER BY iduser DESC limit 1;"""
    cur.execute(query)
    result = cur.fetchall()
    iduser = int(result[0][0]) + 1
    query = """INSERT INTO users (iduser, username) VALUES ({}, '{}') RETURNING {};""".format(iduser, name, 'users.iduser')
    cur.execute(query)
    id = cur.fetchone()[0]
    print(id)
    return json.dumps(id)

@post('/chat/create')
def createChat():
    query = """select idchat from chats order by idchat desc limit 1;"""
    cur.execute(query)
    result = cur.fetchall()
    idchat = int(result[0][0]) + 1
    query = """INSERT INTO chats (idchat) VALUES ({}) RETURNING {};""".format(idchat,'chats.idchat')
    cur.execute(query)
    id = cur.fetchone()[0]
    print("New chat created with chatid:",id)
    return json.dumps(id)

@post('/chat/<chat_id>/addmessage')
def addMessage(chat_id):
    chats_idchat = int(chat_id)
    userid = int(request.forms.get("userid"))
    text = str(request.forms.get("message"))
    print(chats_idchat, userid)
    query = """select idmessage from messages order by idmessage desc limit 1;"""
    cur.execute(query)
    result = cur.fetchall()
    idmessage = int(result[0][0]) + 1
    query = """INSERT INTO messages (idmessage, text, datetime, users_iduser, chats_idchat) VALUES ({}, '{}', to_char(current_timestamp, 'yyyy-mm-dd hh:mi:ss'), {}, {}) RETURNING {};""".format(idmessage, text, userid, chats_idchat, 'messages.idmessage')
    cur.execute(query)
    id = cur.fetchone()[0]
    print(id)
    return json.dumps(id)

port = int(os.getenv("PORT", 8080))
print(f"Running server {port}....")

run(host="0.0.0.0", port=port, debug=True)


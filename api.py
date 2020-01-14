#!/usr/bin/python3
from bottle import route, run, get, post, request, static_file
import psycopg2
import json
import os
import random
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from textblob import TextBlob
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity as distance 

# Connection to Postgresql in Heroku:
DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='require')
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cur = conn.cursor()

@get("/")
def index():
    return {
        "Chat Sentiment Analysis API": "https://github.com/mariobru/chat-sentiment-analysis-service",
        "Created by": "Mario Bru"
    }

# List all messages from a chat
@get("/chat/<chat_id>/list")
def chatMessages(chat_id):
    chatid = int(chat_id)
    query = """SELECT text FROM messages WHERE chats_idchat={};""".format(chatid)
    cur.execute(query)
    result = cur.fetchall()
    return json.dumps(result)

# List all messages a user has written
@get("/user/<user_id>/messages")
def userMessages(user_id):
    query = """SELECT text FROM messages WHERE users_iduser={};""".format(user_id)
    cur.execute(query)
    result = cur.fetchall()
    return json.dumps(result)

# Show the conversations of a chat with datetime, username and text
@get("/chat/<chat_id>/showconv")
def chatConv(chat_id):
    chatid = int(chat_id)
    query = """select m.datetime, u.username, m.text from users u inner join messages m on u.iduser = m.users_iduser where m.chats_idchat={} order by m.datetime asc;""".format(chatid)
    cur.execute(query)
    result = cur.fetchall()
    return json.dumps(result)

# Show the sentiment analysis of a chat
@get("/chat/<chat_id>/sentiment")
def chatSent(chat_id):
    myjson = chatMessages(chat_id)
    messages = json.loads(myjson)
    if len(messages) == 0:
        return json.dumps({"Error": "This chat has no messages."})
    else:
        polarity = 0
        subjectivity = 0
        for e in messages:
            polarity += TextBlob(*e).sentiment[0]
            subjectivity += TextBlob(*e).sentiment[1]
        polarity_mean = polarity/len(messages)
        subjectivity_mean = subjectivity/len(messages)
        return {
            'Polarity': 'is a float value within the range [-1.0 to 1.0] where 0 indicates neutral, +1 indicates a very positive sentiment and -1 represents a very negative sentiment.',
            'Subjectivity': 'is a float value within the range [0.0 to 1.0] where 0.0 is very objective and 1.0 is very subjective. Subjective sentence expresses some personal feelings, views, beliefs, opinions, allegations, desires, beliefs, suspicions, and speculations where as Objective sentences are factual.',
            'Polarity mean of this chat': polarity_mean, 
            'Subjectivity mean of this chat': subjectivity_mean
            }

# Create a new user
@get('/user/create')
def insert_name():
    return '''<form method="POST" action="/user/create">
                Insert a new name: <input name="name"     type="text" />
                <input type="submit" />
              </form>'''


@post('/user/create')
def createUser():
    name = str(request.forms.get("name"))
    try:
        print(name)
        query = """SELECT username FROM users WHERE username='{}'""".format(name)
        cur.execute(query)
        dbname = cur.fetchone()[0]
        print(dbname)
    except:
        dbname = None
    if name == dbname:
        return json.dumps({"Error": "This name already exists! Try a new one ;)"})
    else:
        query = """SELECT iduser FROM users ORDER BY iduser DESC limit 1;"""
        cur.execute(query)
        result = cur.fetchall()
        iduser = int(result[0][0]) + 1
        query = """INSERT INTO users (iduser, username) VALUES ({}, '{}') RETURNING {};""".format(iduser, name, 'users.iduser')
        cur.execute(query)
        id = cur.fetchone()[0]
        print(id)
        return json.dumps(id)

# Create a new chat
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

# Add a message to a chat
@get('/chat/addmessage')
def insert_message():
    return '''<form method="POST" action="/chat/addmessage">
                Insert a user id: <input name="userid"     type="text" />
                Insert a chat id: <input name="chatid"     type="text" />
                Send a comment to the chat: <input name="message"     type="text" />
                <input type="submit" />
              </form>'''

@post('/chat/addmessage')
def addMessage():
    chats_idchat = int(request.forms.get("chatid"))
    userid = int(request.forms.get("userid"))
    text = str(request.forms.get("message"))
    print(chats_idchat, userid)
    query = """select idmessage from messages order by idmessage desc limit 1;"""
    cur.execute(query)
    result = cur.fetchall()
    idmessage = int(result[0][0]) + 1
    query = """INSERT INTO messages (idmessage, text, datetime, users_iduser, chats_idchat) VALUES ({}, '{}', to_char(current_timestamp, 'yyyy-mm-dd hh24:mi:ss'), {}, {}) RETURNING {};""".format(idmessage, text, userid, chats_idchat, 'messages.idmessage')
    cur.execute(query)
    id = cur.fetchone()[0]
    print(id)
    return json.dumps(id)

# Get a recommendation of three users based on what they and you have written on the chats
@get("/user/<user_id>/recommend")
def userRecommend(user_id):
    query = """select username from users where iduser={}""".format(user_id)
    cur.execute(query)
    name = cur.fetchone()[0]
    print(name,type(name))
    data = json.loads(selectTables("users"))
    docs = dict()
    for u in data:
        messages = userMessages(u[0])
        docs.update({u[1]:messages})
    count_vectorizer = CountVectorizer()
    sparse_matrix = count_vectorizer.fit_transform(docs.values())
    doc_term_matrix = sparse_matrix.todense()
    df = pd.DataFrame(doc_term_matrix, columns=count_vectorizer.get_feature_names(), index=docs.keys())
    similarity_matrix = distance(df, df)
    sim_df = pd.DataFrame(similarity_matrix, columns=docs.keys(), index=docs.keys())
    np.fill_diagonal(sim_df.values, 0) # Remove diagonal max values and set those to 0
    res = {'recommended_users': [e for e in list(sim_df[name].sort_values(ascending=False)[0:3].index)]}
    return res


port = int(os.getenv("PORT", 80))
print(f"Running server {port}....")

run(host="0.0.0.0", port=port, debug=True)


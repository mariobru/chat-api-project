#!/usr/bin/python3

import os
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT 

DATABASE_URL = os.environ['DATABASE_URL']
#Connect to DB
conn = psycopg2.connect(DATABASE_URL, sslmode='require')
#If permission Error
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
#Create Cursor
cur = conn.cursor()
#DROP Tables
cur.execute("DROP TABLE IF EXISTS message;DROP TABLE IF EXISTS messages;DROP TABLE IF EXISTS chats;DROP TABLE IF EXISTS users;")

#!/usr/bin/python3

import os
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT 
import argparse

parser = argparse.ArgumentParser(description='Get messages for specific idChat')
parser.add_argument('--id', type=int, help='idChat')
n = parser.parse_args().id
print(n)

URL = 'postgres://ybgqdfwrfktliz:ed949a4fa7a88c55fc89844f3376c3aa59c4d64bde80a54b78b45d8397591960@ec2-46-137-113-157.eu-west-1.compute.amazonaws.com:5432/dckopqv6o4em74'
#DATABASE_URL = os.environ['DATABASE_URL']
#Connect to DB
conn = psycopg2.connect(URL, sslmode='require')
#If permission Error
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
#Create Cursor
cur = conn.cursor()
#Query Data
query = """SELECT * FROM messages WHERE chats_idChat={};""".format(n)
cur.execute(query)
result = cur.fetchall()
print(result)
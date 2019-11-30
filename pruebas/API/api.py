#!/usr/bin/python3
from bottle import route, run, get, post, request
import psycopg2
import bson
import os
import random
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT 

# Connection to Postgresql in Heroku:
URL = 'postgres://ybgqdfwrfktliz:ed949a4fa7a88c55fc89844f3376c3aa59c4d64bde80a54b78b45d8397591960@ec2-46-137-113-157.eu-west-1.compute.amazonaws.com:5432/dckopqv6o4em74'
conn = psycopg2.connect(URL, sslmode='require')
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cur = conn.cursor()
#!/usr/bin/python3


@get("/")
def index():
    return {
        "nombre": random.choice(["Pepe", "Juan", "Fran", "Luis"])
    }

@get("/users")
def getUsers():
    query = """SELECT * FROM users;"""
    cur.execute(query)
    result = cur.fetchall()
    return str(result)


# @get("/chiste/<tipo>")
# def demo2(tipo):#
#     print(f"un chiste de {tipo}")
#     if tipo == "chiquito":
#         return {
#             "chiste": "Van dos soldados en una moto y no se cae ninguno porque van soldados"
#         }
#     elif tipo == "eugenio":
#         return {
#             "chiste": "Saben aquell que diu...."
#         }
#     else:
#         return {
#             "chiste": "No puedorrr!!"
#         }

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


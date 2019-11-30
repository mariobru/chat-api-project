import os
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT 

class PostgresConection:

    def __init__(self, URL):
        self.conn = psycopg2.connect(URL, sslmode='require')
        self.isolation = self.conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        self.cur = self.conn.cursor()

    def addDocument(self,document):
        a=self.collection.insert_one(document)
        print("Inserted", a.inserted_id)
        return a.inserted_id
    
    def addChiste(self, autor, chiste):
        document={'autor':autor,
                'chiste':chiste}
        return self.addDocument(document)
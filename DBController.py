import psycopg2, psycopg2.extras
import threading
from time import sleep
"""
conn = psycopg2.connect(database='test', user='postgres', password='pass', host='localhost')
cur = conn.cursor()
cur.execute("SELECT * FROM estudiante")
rows=cur.fetchall()
print rows

"""


class DBController:
    def __init__(self,dbname,dbuser,dbpasword,dbhost):
        self.conn = psycopg2.connect(
            database=dbname,
            user=dbuser,
            password=dbpasword,
            host=dbhost
        )
        self.cur = self.conn.cursor()

    def executeTest(self,configs):
        pass

    def insertUser(self,config):
        """thread worker function"""
        sleep(config.time)
        print
        'Worker'
        return

    def connection(self, config):

        threads = []
        for i in range(config.connections):
            if config.opertation == "":
                t = threading.Thread(target=self.insertUser(config))
            threads.append(t)
            t.start()

    def insertUsers(self,user):
        self.cur.callproc("newUser" , (
            user.id,
            user.email,
            user.name,
            user.firs_lastname,
            user.second_lastname
        ))

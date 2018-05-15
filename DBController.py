import psycopg2, psycopg2.extras
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

    def insert(self, type):

    def insertUsers(self,user):
        self.cur.callproc("newUser" , (
            user.id,
            user.email,
            user.name,
            user.firs_lastname,
            user.second_lastname
        ))

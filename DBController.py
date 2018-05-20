import psycopg2, psycopg2.extras, threading, random, Objects, time
from time import sleep

"""
conn = psycopg2.connect(database='test', user='postgres', password='pass', host='localhost')
cur = conn.cursor()
cur.execute("SELECT * FROM estudiante")
rows=cur.fetchall()
print rows

"""


class DBController:
    def __init__(self, dbname, dbuser, dbpasword, dbhost):
       self.testResultsList = []
       self.conn = psycopg2.connect("dbname=" + dbname + " user=" + dbuser + " password=" + dbpasword + " host=" + dbhost)



    def insertReserva(self):
        usuario=random.randint(1, 100)
        sede=random.randint(1, 2)
        costo=random.randint(200000, 100000)
        servicio=random.randint(1, 8)
        cantidad=random.randint(1, 20)
        cur = self.conn.cursor()
        cur.execute("select insReservacion(%d,%d,%d,%d,%d)" % (usuario, sede,costo,servicio,cantidad))
        self.conn.commit()
        cur.close()
        return

    def deleteReserva(self,id):
        cur = self.conn.cursor()
        cur.execute("select delReservacion("+id+")")
        self.conn.commit()
        cur.close()
        return


    def updateReserva(self):
        p_idReserva=random.randint(0, 100)
        p_idServicio=random.randint(1, 6)
        p_cantidad=random.randint(1, 20)
        cur = self.conn.cursor()
        cur.execute("select updReservacion(%d,%d,%d)" % (p_idReserva, p_idServicio,p_cantidad))
        self.conn.commit()
        cur.close()
        return


    def ingresosSede(self):
        p_idSede=random.randint(1, 2)
        p_fechaA='2018-01-01'
        p_fechaB='2019-12-30'
        cur = self.conn.cursor()
        cur.execute("select ingresosSede(%d,%s,%s,%d)" % (p_idSede,p_fechaA,p_fechaB,0))
        self.conn.commit()
        cur.close()
        return

    def connection(self, config):
        threads = []
        id = 0
        for i in range(config.connections):
            i += 1
            operation = random.randint(0, 3)
            print(operation)
            if operation == 0:
                t = threading.Thread(target=self.insertReserva())
            elif operation == 1:
                t = threading.Thread(target=self.preInsertUser(config))
            elif operation == 2:
                t = threading.Thread(target=self.preInsertUser(config))
            else:
                t = threading.Thread(target=self.preInsertUser(config))
            t0 = time.time()

            print(t0)
            t0=0


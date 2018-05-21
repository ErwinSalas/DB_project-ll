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

    def deleteReserva(self):
        cur = self.conn.cursor()
        cur.execute("select delReservacion()")
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

    def addIndexDateOnCentralDB(self):
        connIndex = psycopg2.connect("dbname=centralDB user=postgres password=password host=localhost")
        curr = connIndex.cursor()
        curr.execute("CREATE index idx_fecha_reservas on reservas(fecha)")
        connIndex.commit()
        curr.close()
        connIndex.close()
        t0 = time.time()
        self.
        timeOnProcedureWithIndex = time.time() - t0
        self.deleteIndexDateOnCentralDB()

    def deleteIndexDateOnCentralDB(self):
        connIndex = psycopg2.connect("dbname=centralDB user=postgres password=password host=localhost")
        curr = connIndex.cursor()
        curr.execute("DROP index idx_fecha_reservas")
        connIndex.commit()
        curr.close()
        connIndex.close()

    def addIndexServiceTypeOnNodeIII(self):
        connIndex = psycopg2.connect("dbname=nodeIII user=postgres password=password host=localhost")
        curr = connIndex.cursor()
        curr.execute("CREATE index idx_tipo_servicio on servicios(tipo)")
        connIndex.commit()
        curr.close()
        connIndex.close()

    def deleteIndexServiceTypeOnNodeIII(self):
        connIndex = psycopg2.connect("dbname=nodeIII user=postgres password=password host=localhost")
        curr = connIndex.cursor()
        curr.execute("DROP index idx_tipo_servicio")
        connIndex.commit()
        curr.close()
        connIndex.close()

    def addIndexServiceReservesOnNodeIII(self):
        connIndex = psycopg2.connect("dbname=nodeIII user=postgres password=password host=localhost")
        curr = connIndex.cursor()
        curr.execute("CREATE index idx_costo_serviciosreservas on servicios_reservas(costo)")
        connIndex.commit()
        curr.close()
        connIndex.close()

    def deleteIndexServiceReservesOnNodeIII(self):
        connIndex = psycopg2.connect("dbname=nodeIII user=postgres password=password host=localhost")
        curr = connIndex.cursor()
        curr.execute("DROP index idx_costo_serviciosreservas ")
        connIndex.commit()
        curr.close()
        connIndex.close()

    def addIndexPrefferedUserOnNodeIII(self):
        connIndex = psycopg2.connect("dbname=nodeIII user=postgres password=password host=localhost")
        curr = connIndex.cursor()
        curr.execute("CREATE index idx_usr_pref on usuarios(preferencia)")
        connIndex.commit()
        curr.close()
        connIndex.close()

    def deleteIndexPrefferedUserOnNodeIII(self):
        connIndex = psycopg2.connect("dbname=nodeIII user=postgres password=password host=localhost")
        curr = connIndex.cursor()
        curr.execute("DROP index idx_usr_pref")
        connIndex.commit()
        curr.close()
        connIndex.close()

    def addIndexServiceTypeOnNodeII(self):
        connIndex = psycopg2.connect("dbname=nodeII user=postgres password=password host=localhost")
        curr = connIndex.cursor()
        curr.execute("CREATE index idx_tipo_servicio on servicios(tipo)")
        connIndex.commit()
        curr.close()
        connIndex.close()

    def deleteIndexServiceTypeOnNodeII(self):
        connIndex = psycopg2.connect("dbname=nodeII user=postgres password=password host=localhost")
        curr = connIndex.cursor()
        curr.execute("DROP index idx_tipo_servicio")
        connIndex.commit()
        curr.close()
        connIndex.close()

    def addIndexServiceReservesOnNodeII(self):
        connIndex = psycopg2.connect("dbname=nodeII user=postgres password=password host=localhost")
        curr = connIndex.cursor()
        curr.execute("CREATE index idx_costo_serviciosreservas on servicios_reservas(costo)")
        connIndex.commit()
        curr.close()
        connIndex.close()

    def deleteIndexServiceReservesOnNodeII(self):
        connIndex = psycopg2.connect("dbname=nodeII user=postgres password=password host=localhost")
        curr = connIndex.cursor()
        curr.execute("DROP index idx_costo_serviciosreservas ")
        connIndex.commit()
        curr.close()
        connIndex.close()

    def addIndexPrefferedUserOnNodeII(self):
        connIndex = psycopg2.connect("dbname=nodeII user=postgres password=password host=localhost")
        curr = connIndex.cursor()
        curr.execute("CREATE index idx_usr_pref on usuarios(preferencia)")
        connIndex.commit()
        curr.close()
        connIndex.close()

    def deleteIndexPrefferedUserOnNodeII(self):
        connIndex = psycopg2.connect("dbname=nodeII user=postgres password=password host=localhost")
        curr = connIndex.cursor()
        curr.execute("DROP index idx_usr_pref")
        connIndex.commit()
        curr.close()
        connIndex.close()

    def connection(self, config):
        for numConection in range(config.connections):
            numConection += 1
            for numOperation in range(config.operations):
                numOperation += 1
                time.sleep(config.time)
                t0 = time.time()
                operation = random.randint(0, 3)
                if operation == 0:
                    t = threading.Thread(target=self.insertReserva())
                elif operation == 1:
                    t = threading.Thread(target=self.updateReserva())
                elif operation == 2:
                    t = threading.Thread(target=self.deleteReserva())
                else:
                    t = threading.Thread(target=self.ingresosSede())
                t.start()
                timeOnProcedure = time.time() - t0
                print(time.time() - t0)
                Objects.TestResult(numConection, numOperation, operation, timeOnProcedure)
        self.conn.close()

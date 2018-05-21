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
        costo=random.randint(20000, 100000)
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

    #Consulta de usuarios por preferencia
    def usuariosPorPreferencia(self):
        cur = self.conn.cursor()
        cur.execute(" select uc.idUsuario, uc.nombre from usuarios uc inner join"+
                    " (select * from dblink('host=localhost user=postgres password=postgres dbname=nodeII',"+
           " 'select * from usuarios u where u.preferencia = ''tipo1'' ') as"+
                    " usr_node(idUsuario int, email varchar(20),psswrd varchar(10),preferencia varchar(15)) limit 200) "+
                    "usr_nodeII on uc.idUsuario=usr_nodeII.idUsuario "+
                    "inner join"+
                    "(select * from dblink('host=localhost user=postgres password=postgres dbname=nodeiii',"+
            "'select * from usuarios u where u.preferencia = ''tipo1'' ') as"+
        " usr_node(idUsuario int,email varchar(20), psswrd varchar(10), preferencia varchar(15)) limit 200)usr_nodeIII on uc.idUsuario = usr_nodeIII.idUsuario; --asignar para una preferencia de un usuario espec")
        self.conn.commit()
        cur.close()
        return

    # Consulta de usuarios por preferencia
    def servisiosMasCaros(self):
        cur = self.conn.cursor()
        cur.execute(" select uc.idUsuario, uc.nombre from usuarios uc inner join"+
    "(select * from dblink('host=localhost user=postgres password=postgres dbname=nodeii',"+
            "'select * from usuarios u where u.preferencia = ''tipo1'' ') as"
            "usr_node(idUsuario int,email varchar(20),psswrd varchar(10),preferencia varchar(15)) limit 200) usr_nodeII on uc.idUsuario=usr_nodeII.idUsuario "+
   " inner join"+
    "(select * from dblink('host=localhost user=postgres password=postgres dbname=nodeiii',"+
            "'select * from usuarios u where u.preferencia = ''tipo1'' ') as"+
            "usr_node(idUsuario int, email varchar(20), psswrd varchar(10),preferencia varchar(15)) limit 200)usr_nodeIII on uc.idUsuario = usr_nodeIII.idUsuario; --asignar para una preferencia de un usuario espec")
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

                result = Objects.TestResult(0,0,0,0)
                result.id = numConection
                result.threadConection = numOperation

                time.sleep(config.time)
                t0 = time.time()
                operation = random.randint(0, 5)
                if operation == 0:
                    t = threading.Thread(target=self.insertReserva())
                    result.operation="insertReserva()"
                elif operation == 1:
                    t = threading.Thread(target=self.updateReserva())
                    result.operation = "updateReserva()"
                elif operation == 2:
                    t = threading.Thread(target=self.deleteReserva())
                    result.operation = "deleteReserva()"

                elif operation == 3:
                    t = threading.Thread(target=self.servisiosMasCaros())
                    result.operation = "servisiosMasCaros()"

                elif operation == 4:
                    t = threading.Thread(target=self.usuariosPorPreferencia())
                    result.operation = "usuariosPorPreferencia()"

                else:
                    t = threading.Thread(target=self.ingresosSede())
                    result.operation = "ingresosSede()"

                t.start()
                timeOnProcedure = time.time() - t0
                print(time.time() - t0)
                result.time=timeOnProcedure
                self.testResultsList.append(result)
        self.conn.close()
        return self.testResultsList

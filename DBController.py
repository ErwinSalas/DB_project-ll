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
        cur = self.conn.cursor()
        cur.execute("select insReservacionN(1);")
        cur.close()
        return

    def deleteReserva(self):
        cur = self.conn.cursor()
        cur.execute("select delReservacion()")
        cur.close()
        return

    #Consulta de usuarios por preferencia
    def usuariosPorPreferencia(self):
        cur = self.conn.cursor()
        cur.execute(" select uc.idUsuario, uc.nombre from usuarios uc inner join"+
                    " (select * from dblink('host=localhost user=postgres password=aniram dbname=nodeII',"+
           " 'select * from usuarios u where u.preferencia = ''tipo1'' ') as"+
                    " usr_node(idUsuario int, email varchar(20),psswrd varchar(10),preferencia varchar(15)) limit 200) "+
                    "usr_nodeII on uc.idUsuario=usr_nodeII.idUsuario"+
                    " inner join "+
                    "(select * from dblink('host=localhost user=postgres password=aniram dbname=nodeIII',"+

            "'select * from usuarios u where u.preferencia = ''tipo1'' ') as"+
        " usr_node(idUsuario int,email varchar(20), psswrd varchar(10), preferencia varchar(15)) limit 200)usr_nodeIII on uc.idUsuario = usr_nodeIII.idUsuario; --asignar para una preferencia de un usuario espec")
        result = cur.fetchall()
        cur.close()
        return result

    # Consulta de usuarios por preferencia
    def servisiosMasCaros(self):
        cur = self.conn.cursor()
        cur.execute(" select uc.idUsuario, uc.nombre from usuarios uc inner join "+
    "(select * from dblink('host=localhost user=postgres password=aniram dbname=nodeII',"+
            "'select * from usuarios u where u.preferencia = ''tipo1'' ') as "
            "usr_node(idUsuario int,email varchar(20),psswrd varchar(10),preferencia varchar(15)) limit 200) usr_nodeII on uc.idUsuario=usr_nodeII.idUsuario"+
   " inner join "+
    "(select * from dblink('host=localhost user=postgres password=aniram dbname=nodeIII',"+
            "'select * from usuarios u where u.preferencia = ''tipo1'' ') as "+
            "usr_node(idUsuario int, email varchar(20), psswrd varchar(10),preferencia varchar(15)) limit 200)usr_nodeIII on uc.idUsuario = usr_nodeIII.idUsuario; --asignar para una preferencia de un usuario espec")
        result = cur.fetchall()
        cur.close()
        return result

    def updateReserva(self):
        cur = self.conn.cursor()
        cur.execute("select updReservacion()")
        cur.close()
        return

    def ingresosSede(self):
        p_idSede=random.randint(1, 2)
        p_fechaA="01-10-2018"
        cur = self.conn.cursor()
        cur.execute("select ingresosSede(%d,'%s')" % (p_idSede,p_fechaA))
        self.conn.commit()
        cur.close()
        return



    def getSizes(self,db):
        cur = self.conn.cursor()
        cur.execute("select consultarBD('"+db+"')")
        result = cur.fetchall()
        cur.close()
        return result[0][0]

    def getOldSizes(self, result):
        result.centralSizeV = self.getSizes("centralDB")
        result.nodeiiSizeV = self.getSizes("nodeII")
        result.nodeiiiSizeV = self.getSizes("nodeIII")

    def getNewSizes(self, result):
        result.centralSizeN = self.getSizes("centralDB")
        result.nodeiiSizeN = self.getSizes("nodeII")
        result.nodeiiiSizeN = self.getSizes("nodeIII")

    def procedures(self, numConection, config):
        for numOperation in range(config.operations):
            numOperation += 1
            result = Objects.TestResult(numOperation, numConection, "", "no", 0, 0, 0, 0, 0, 0, 0)
            result.id = numConection
            result.threadConection = numOperation
            time.sleep(config.time)
            t0 = time.time()
            operation = 0  # random.randint(0, 5)
            if operation == 0:
                self.getOldSizes(result)
                self.insertReserva()
                self.getNewSizes(result)
                result.operation = "insertReserva()"
            elif operation == 1:
                self.getOldSizes(result)
                self.updateReserva()
                self.getNewSizes(result)
                result.operation = "updateReserva()"
            elif operation == 2:
                self.getOldSizes(result)
                self.deleteReserva()
                self.getNewSizes(result)
                result.operation = "deleteReserva()"

            elif operation == 3:
                t = threading.Thread(target=self.servisiosMasCaros())
                result.operation = "servisiosMasCaros()"
                t.start()
                timeOnProcedure = time.time() - t0
                result.time = timeOnProcedure
                central = self.getSizes("centralDB")
                node2 = self.getSizes("nodeII")
                node3 = self.getSizes("nodeIII")
                result.centralSize = central
                result.nodeiiSize = node2
                result.nodeiiiSize = node3
                self.testResultsList.append(result)

                result = Objects.TestResult(numOperation, numConection, "", "si", 0, 0, 0, 0)
                result.id = numConection
                result.threadConection = numOperation
                result.operation = "servisiosMasCaros()"
                self.addIndexDateOnCentralDB()
                self.addIndexPrefferedUserOnNodeII()
                self.addIndexPrefferedUserOnNodeIII()
                t0 = time.time()


            elif operation == 4:
                t = threading.Thread(target=self.usuariosPorPreferencia())
                result.operation = "usuariosPorPreferencia()"

            else:
                t = threading.Thread(target=self.ingresosSede())
                result.operation = "ingresosSede()"

            timeOnProcedure = time.time() - t0
            result.time = timeOnProcedure
            self.testResultsList.append(result)

    def connection(self, config):
        self.insertReserva()
        for numConection in range(config.connections):
            numConection += 1
            t = threading.Thread(target=self.procedures(numConection, config))
            t.start()
        return self.testResultsList

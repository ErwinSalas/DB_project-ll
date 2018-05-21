import psycopg2


class IndexContoller:
    def __init__(self):
        pass

    def deleteAll(self):
        self.deleteIndexDateOnCentralDB()
        self.deleteIndexPrefferedUserOnNodeII()
        self.deleteIndexPrefferedUserOnNodeIII()
        self.deleteIndexServiceReservesOnNodeII()
        self.deleteIndexServiceReservesOnNodeIII()
        self.deleteIndexServiceTypeOnNodeII()
        self.deleteIndexServiceTypeOnNodeIII()

    def createAll(self):
        self.addIndexDateOnCentralDB()
        self.addIndexPrefferedUserOnNodeII()
        self.addIndexPrefferedUserOnNodeIII()
        self.addIndexServiceReservesOnNodeII()
        self.addIndexServiceReservesOnNodeIII()
        self.addIndexServiceTypeOnNodeII()
        self.addIndexServiceTypeOnNodeIII()


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
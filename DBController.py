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
        # self.namesList = ["María", "Mireya", "Enrique", "José", "Tomás", "Jesús", "Salvador", "Enrique", "Gerardo",
        #                   "Alfonso", "Celina", "Gabriel", "Ángeles"]
        # self.lastnamesList = ["Acevedo", "Manríquez", "Mejía", "Aguilar", "Santana", "Ruiz", "Carolina", "Acosta",
        #                       "López",
        #                       "Canto", "Gámez", "Castellanos", "Ángeles"]
        # self.emailsList = ["julianaparis@hotmail.com", "dcanas@idiomas.udea.edu.co", "jhutado@ idomas.udea.edu.co ",
        #                    "reinald_34@hotmail.com", "ibrahin@cied.rimed.cu", "hersy@epm.net.co",
        #                    "domini26@latinmail.com",
        #                    "m.fdez_87@hotmail.com", "menadel@hotmail.com", "andresiocarga@hotmail.com",
        #                    "vivian_981@yahoo.com"]
        # self.passwordsList = ["asdf", "lkjh", "l,kjnb", "4rfv53", "mnb", "trgf", "jmhtn", "65yt", "nrgdbfs", "ASCD",
        #                       "njhtsrbegf",
        #                       " mnhb", ",lkmjhgf", "3wer", "6uyjh", "mjhb", "rgtf", "6y7uj", "tgdf", "vsdc", "NHFV",
        #                       "bdg sz", ]
        self.testResultsList = []
        self.conn = psycopg2.connect("dbname=" + dbname + " user=" + dbuser + " password=" + dbpasword + " host=" + dbhost)

    def executeTest(self, configs):
        pass

    def insertUsers(self):
        cur = self.conn.cursor()
        cur.execute("select insUsr(20)")
        self.conn.commit()
        cur.close()
        return

    def insServicio(self):
        cur = self.conn.cursor()
        cur.execute("select insServicio(20)")
        self.conn.commit()
        cur.close()
        return

    # def createRandomUser(self):
    #     name = self.namesList[random.randint(0, len(self.namesList)-1)]
    #     lastName1 = self.lastnamesList[random.randint(0, len(self.lastnamesList)-1)]
    #     lastName2 = self.lastnamesList[random.randint(0, len(self.lastnamesList)-1)]
    #     email = self.emailsList[random.randint(0, len(self.emailsList)-1)]
    #     password = self.passwordsList[random.randint(0, len(self.passwordsList)-1)]
    #     user = Objects.User(name, lastName1, lastName2, email, password)
    #     return user

    def preInsertUser(self, config):
        sleep(config.time)
        #user = self.createRandomUser()

        self.insertUsers()
        return

    def connection(self, config):
        threads = []
        self.insertUsers()
        self.conn.close()
        # id = 0
        # for i in range(config.connections):
        #     i += 1
        #     operation = random.randint(0, 3)
        #     print(operation)
        #     if operation == 0:
        #         t = threading.Thread(target=self.preInsertUser(config))
        #     elif operation == 1:
        #         t = threading.Thread(target=self.preInsertUser(config))
        #     elif operation == 2:
        #         t = threading.Thread(target=self.preInsertUser(config))
        #     else:
        #         t = threading.Thread(target=self.preInsertUser(config))
        #     t0 = time.time()
        #
        #     print(t0)
        #     t0=0


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
    def __init__(self,dbname,dbuser,dbpasword,dbhost):
        self.namesList = ["María","Mireya","Enrique","José","Tomás","Jesús","Salvador","Enrique","Gerardo",
                          "Alfonso","Celina","Gabriel","Ángeles"]
        self.lastnamesList = ["Acevedo","Manríquez","Mejía","Aguilar","Santana","Ruiz","Carolina","Acosta","López",
                          "Canto","Gámez","Castellanos","Ángeles"]
        self.emailsList = ["julianaparis@hotmail.com","dcanas@idiomas.udea.edu.co","jhutado@ idomas.udea.edu.co ",
                           "reinald_34@hotmail.com","ibrahin@cied.rimed.cu","hersy@epm.net.co","domini26@latinmail.com",
                          "m.fdez_87@hotmail.com","menadel@hotmail.com","andresiocarga@hotmail.com","vivian_981@yahoo.com"]
        self.passwordsList = ["asdf", "lkjh", "l,kjnb", "4rfv53", "mnb", "trgf", "jmhtn", "65yt", "nrgdbfs", "ASCD", "njhtsrbegf",
                              " mnhb", ",lkmjhgf", "3wer", "6uyjh", "mjhb", "rgtf", "6y7uj", "tgdf", "vsdc", "NHFV", "bdg sz", ]
        self.timersList = []
        self.conn = psycopg2.connect(
            database=dbname,
            user=dbuser,
            password=dbpasword,
            host=dbhost
        )
        self.cur = self.conn.cursor()

    def executeTest(self,configs):
        pass

    def insertUsers(self,user):
        try:
            self.cur.callproc("newUser", (
                user.email,
                user.password,
                user.name,
                user.lastName1,
                user.lastName2
            ))
            print("insertado")
        except:
            print("error")

    def createRandomUser(self):
        name = self.namesList[random.randint(0, len(self.namesList))]
        lastName1 = self.lastnamesList[random.randint(0, len(self.lastnamesList))]
        lastName2 = self.lastnamesList[random.randint(0, len(self.lastnamesList))]
        email = self.emailsList[random.randint(0, len(self.emailsList))]
        password = self.passwordsList[random.randint(0, len(self.passwordsList))]
        user = Objects.User(name, lastName1, lastName2, email, password)
        self.insertUsers(user)

    def preInsertUser(self,config):
        threads = []
        for i in range(config.operation_number):
            sleep(config.time)
            t0 = time.time()
            user = self.createRandomUser()
            t = threading.Thread(target=self.insertUsers(user))
            threads.append(t)
            t.start()
            t1 = time.time()
            totalTime = t1 - t0
            self.timersList.append(totalTime)
            t0 = 0
            t1 = 0
        return

    def connection(self, config):
        threads = []
        id = 0
        self.createRandomUser()
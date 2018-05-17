class Configs:
    def __init__(self,connections,time):
        self.time = time
        self.connections=connections

class User:
    def __init__(self,email, psswrd, nombre, apellido1, apellido2):
        self.email = email
        self.psswrd = psswrd
        self.nombre = nombre
        self.apellido1 = apellido1
        self.apellido2 = apellido2

class TestResult:
    def __init__(self, id, operation):
        self.id = id
        self.time = 0
        self.operation = operation
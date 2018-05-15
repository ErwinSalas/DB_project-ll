class Configs:
    def __init__(self,connections,time,operation,operation_number):
        self.opertation=operation
        self.time = time
        self.connections=connections
        self.operation_number=operation_number

class User:
    def __init__(self,email, psswrd, nombre, apellido1, apellido2):
        self.email = email
        self.psswrd = psswrd
        self.nombre = nombre
        self.apellido1 = apellido1
        self.apellido2 = apellido2


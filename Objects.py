class Configs:
    def __init__(self,connections,time,operation,operation_number):
        self.opertation=operation
        self.time = time
        self.connections=connections
        self.operation_number=operation_number

class User:
    def __init__(self,connections,time,operation):
        self.opertation=operation
        self.time = time
        self.connections=connections


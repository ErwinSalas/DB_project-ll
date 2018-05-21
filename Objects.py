class Configs:
    def __init__(self,connections,time,operations):
        self.time = time
        self.operations=operations
        self.connections=connections

class User:
    def __init__(self,email, psswrd, nombre, apellido1, apellido2):
        self.email = email
        self.psswrd = psswrd
        self.nombre = nombre
        self.apellido1 = apellido1
        self.apellido2 = apellido2

class TestResult:
    def __init__(self, id, threadConection, operation, hasIndex, time, centralSizeV, nodeiiSizeV, nodeiiiSizeV, centralSizeN, nodeiiSizeN, nodeiiiSizeN):
        self.id = id
        self.threadConection = threadConection
        self.operation = operation
        self.hasIndex = hasIndex
        self.time = time
        self.centralSizeV = centralSizeV
        self.nodeiiSizeV = nodeiiSizeV
        self.nodeiiiSizeV = nodeiiiSizeV
        self.centralSizeN = centralSizeN
        self.nodeiiSizeN = nodeiiSizeN
        self.nodeiiiSizeN = nodeiiiSizeN

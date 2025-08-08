class Departamento(): 
    def __init__(self, id, name): 
        self.id = id 
        self.name = name

    def show(self): 
        """
        Metodo para imprimir los atributos del objeto departamento
        """
        print(f'\n ID: {self.id}, Nombre: {self.name}')
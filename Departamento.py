class Departamento(): 
    def __init__(self, id, name): 
        self.id = id 
        self.name = name

    def show(self): 
        print(f'ID: {self.id}, Nombre: {self.name}')
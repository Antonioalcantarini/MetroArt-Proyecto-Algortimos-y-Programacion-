import requests
from Departamento import Departamento
from Obra import Obra

class App(): 

    def menu (self, list): 

        for index, opcion in enumerate(list): 
            print (f'{index + 1} - {opcion}')

        seleccion_opcion = input('Ingrese el número de opción: ') 
        while not seleccion_opcion.isnumeric() or not int(seleccion_opcion) in range(1, len(list)+1):
            seleccion_opcion = input('Error, ingrese una opción válida:  ')

        return int(seleccion_opcion) - 1
    
    def start(self): 

        while True: 
            opciones = ["Elegir departamento de obras", "Busqueda de obras", "Mostrar detalles de la obra", "Salir"]
            opcion_escogida = self.menu(opciones)

            if opcion_escogida == 0: 
                # if not self.departamentos: 
                    self.cargar_departamentos()
                    for departamento in self.departamentos: 
                        departamento.show()
                        print()
                    self.Id_elegido = input("Elija el Id del departamento que desea cargar: ") 
                    while not self.Id_elegido.isnumeric or not int(self.Id_elegido) in range (1, len(self.departamentos)-1): 
                        self.Id_elegido = input("El id seleccionado no es válido, por favor seleccione un id dentro de los encontrados: ")
                    for departamento in self.departamentos: 
                        if int(self.Id_elegido) == departamento.id: 
                            self.cargar_obras()
                            for obra in self.obras: 
                                obra.show()
                                print()
                # else: 
                #     self.Id_elegido = input("Elija el Id del departamento que desea cargar")
                #     while not self.Id_elegido.isnumeric or not int(self.Id_elegido) in range (1, len(self.departamentos)+1): 
                #         self.Idelegido = input("El id seleccionado no es válido, por favor seleccione un id dentro de los encontrados")
                #     for departamento in self.departamentos: 
                #         if self.Id_elegido == departamento.id: 
                #             self.cargar_obras()

                

                
    def cargar_departamentos(self): 
        self.departamentos = [] 
        depas = requests.get("https://collectionapi.metmuseum.org/public/collection/v1/departments")
        departamentos_dic = depas.json()["departments"]

        for departamento in departamentos_dic: 
            self.departamentos.append(Departamento(departamento["departmentId"], departamento["displayName"]))


    def cargar_obras(self): 
        self.obras = []
        objetos = requests.get(f"https://collectionapi.metmuseum.org/public/collection/v1/objects?departmentIds={self.Id_elegido}")
        obras_Id = objetos.json()["objectIDs"]

        for id in obras_Id: 
            obra = requests.get(f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{id}")
            print(obra.text)
            try: 
                obra_dic = obra.json()
                self.obras.append(Obra(obra_dic["title"], obra_dic["artistDisplayName"],obra_dic["artistNationality"], obra_dic["artistBeginDate"], obra_dic["artistEndDate"], obra_dic["classification"], obra_dic["objectDate"], obra_dic["primaryImage"]))
            except ValueError: 
                print(f"{id} no valido")



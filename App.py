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

        self.obras = []
        self.departamentos = []
        self.departamentos_busq = []
        self.lista_ids_departamentos = []
        self.lista_ids_departamentos_busq = []

        self.cargar_csv()
        self.cargar_departamentos() 


        while True: 
            opciones = ["Elegir departamento de obras", "Busqueda de obras", "Mostrar detalles de la obra", "Salir"]
            opcion_escogida = self.menu(opciones)

            if opcion_escogida == 0: 
                for departamento in self.departamentos: 
                    departamento.show()
                print()
                Id_elegido = input("Elija el Id del departamento que desea cargar: ")
                while not Id_elegido.isnumeric() or int(Id_elegido) not in self.lista_ids_departamentos:  
                    Id_elegido = input("El id seleccionado no es válido, por favor seleccione un id dentro de los encontrados: ")
                for departamento in self.departamentos: 
                    if int(Id_elegido) == departamento.id: 
                        self.departamentos.remove(departamento)
                        self.departamentos_busq.append(departamento)
                        self.cargar_obras(Id_elegido)
                        print("Obras guradadas exitosamente \n")
            if opcion_escogida == 1:  
                if not self.obras: 
                    print("\n No se encuentran obras guardadas actualmente, por favor elija un departamento de obras para poder iniciar la busqueda\n")
                else:
                    for departamento in self.departamentos_busq: 
                        self.lista_ids_departamentos_busq.append(departamento.id)
                    while True:
                        opciones_busqueda = ["Lista de obras por departamento", "Lista de por nacionalidad del autor", "Lista de obras por nombre del autor", "Salir de la busqueda"]
                        opcion_seleccionada = self.menu(opciones_busqueda)

                        if opcion_seleccionada == 0: 
                            for departamento in self.departamentos_busq: 
                                departamento.show()
                                print()
                            Id_seleccionado = input("Elija el id del departamento cuyas obras desea visualizar: ")
                            while not Id_seleccionado.isnumeric() or int(Id_seleccionado) not in self.lista_ids_departamentos_busq: 
                                Id_seleccionado = input("Error, input inválido. Elija un valor numérico: " ) 
                            for departamento in self.departamentos_busq: 
                                if int(Id_seleccionado) == departamento.id: 
                                    for obra in self.obras:
                                        if int(Id_seleccionado) == obra.id_departamento:
                                            obra.show_busqueda()
                                            print() 
                        
                        if opcion_seleccionada == 1: #Probar mediante departamento 4 
                                nacionalidad_escogida = self.menu(self.lista_países)
                                nacionalidad_string = self.lista_países[nacionalidad_escogida]
                                for obra in self.obras: 
                                    if nacionalidad_string == obra.nacionalidad_artista: 
                                        obra.show_busqueda()
                                        print()

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
            self.lista_ids_departamentos.append(departamento["departmentId"])


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
    
    def cargar_csv(self): 
        df = pd.read_csv(r"C:\Users\Usuario\Desktop\CH_Nationality_List_20171130_v1.csv")
        self.lista_países = df["Nationality"].values.tolist()



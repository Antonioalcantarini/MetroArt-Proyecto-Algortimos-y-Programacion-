import requests
from Departamento import Departamento
from Obra import Obra
from PIL import Image
import pandas as pd
import time

class App(): 

    def menu (self, list): 
        """"
        Función básica de menu que permite seleccionar una de las opciones estipuladas dentro de una lista que es utilizada como parámetro
        """

        for index, opcion in enumerate(list): 
            print (f'{index + 1} - {opcion}')

        seleccion_opcion = input('Ingrese el número de opción: ') 
        while not seleccion_opcion.isnumeric() or not int(seleccion_opcion) in range(1, len(list)+1):
            seleccion_opcion = input('Error, ingrese una opción válida:  ')

        return int(seleccion_opcion) - 1
    
    def start(self): 
        """ 
        Función principal donde se desarrollan todas las funciones del programa. 
        """

        #Se crean todas las listas necesarias para el correcto funcionamiento de la app.
        self.obras = []
        self.departamentos = []
        self.departamentos_busq = []
        self.lista_ids_departamentos = []
        self.lista_ids_departamentos_busq = []
        self.lista_ids_obras = []

        #Se carga el csv y todos los departamentos de la API sin sus obras.
        self.cargar_csv()
        self.cargar_departamentos()

        #Se crean todas las listas de opciones necesarias para los menus generales. 
        opciones = ["Elegir departamento de obras", "Busqueda de obras", "Mostrar detalles de la obra", "Salir"]
        opciones_apellidos = ["Un apellido",  "Dos apellidos"]
        self.opciones_binarias = ["Si", "No"]

        print("\n IMPORTANTE: No podrá realizar la búsqueda de obras o mostrar detalles de las mismas sin haber elegido un departamento\n")

        while True: 
            opcion_escogida = self.menu(opciones)
            
            #Módulo 1: Selección del departamento para la carga de obras
            if opcion_escogida == 0: 
                #Se verifica que existan departamentos en la lista 'Self.deparatamentos'
                if not self.departamentos: 
                    print("\nTodos los departamentos ya se encuentran cargados. Por favor, realice una búsqueda\n")
                else: 
                    for departamento in self.departamentos: 
                        departamento.show()
                    print()
                    Id_elegido = input("\nElija el Id del departamento que desea cargar: ")
                    while not Id_elegido.isnumeric() or int(Id_elegido) not in self.lista_ids_departamentos:  
                        Id_elegido = input("\nEl id seleccionado no es válido, por favor seleccione un id dentro de los encontrados: ")
                    for departamento in self.departamentos: 
                        if int(Id_elegido) == departamento.id: 
                            #Se elimina el departamento seleccionado de la lista de departamentos cargados
                            self.departamentos.remove(departamento)
                            #Se elimina el id seleccionado de la lista de departamentos cargados
                            self.lista_ids_departamentos.remove(departamento.id)
                            #Se agrega el departamento a la lista de departamentos que se pueden buscar mediante el módulo 2
                            self.departamentos_busq.append(departamento)
                            #Se llama a la función cargar obras
                            self.cargar_obras(Id_elegido)
                            print("\nObras guardadas exitosamente\n")
                        
            #Módulo 2: Búsqueda de obras
            if opcion_escogida == 1: 
                #Se verifica que existan obras cargadas para poder realizar la busqueda de obras
                if not self.obras: 
                    print("\nNo se encuentran obras guardadas actualmente, por favor elija un departamento de obras para poder iniciar la busqueda\n")
                else:
                    print("\nBienvenido al módulo de búsqueda. Ingrese el número la opción mediante el cual desea realizar su busqueda\n")
                    for departamento in self.departamentos_busq: 
                        self.lista_ids_departamentos_busq.append(departamento.id)
                    while True:
                        opciones_busqueda = ["Lista de obras por departamento", "Lista de por nacionalidad del autor", "Lista de obras por nombre del autor", "Salir de la busqueda"]
                        opcion_seleccionada = self.menu(opciones_busqueda)

                        #Punto a. del módulo de Búsqueda: 
                        if opcion_seleccionada == 0: 
                            for departamento in self.departamentos_busq: 
                                #Se llama al método show de la clase departamento
                                departamento.show()
                            print()
                            Id_seleccionado = input("\nElija el id del departamento cuyas obras desea visualizar: ")
                            while not Id_seleccionado.isnumeric() or int(Id_seleccionado) not in self.lista_ids_departamentos_busq: 
                                Id_seleccionado = input("\nError, input inválido. Elija un valor numérico: " ) 
                            for departamento in self.departamentos_busq: 
                                if int(Id_seleccionado) == departamento.id: 
                                    for obra in self.obras:
                                        if int(Id_seleccionado) == obra.id_departamento:
                                            #Se llama al método Show_busqueda de la clase obra
                                            obra.show_busqueda()
                                            print() 

                        #Punto b. del módulo de Búsqueda: 
                        if opcion_seleccionada == 1: 
                                encontrado_nacionalidad = False
                                nacionalidad_escogida = self.menu(self.lista_países)
                                nacionalidad_string = self.lista_países[nacionalidad_escogida]
                                for obra in self.obras: 
                                    if nacionalidad_string == obra.nacionalidad_artista:
                                        encontrado_nacionalidad = True
                                        #Se llama al método Show_busqueda de la clase obra 
                                        obra.show_busqueda()
                                        print()
                                    else: 
                                        if encontrado_nacionalidad == False and obra == self.obras[-1]: 
                                            print(f"\n No se ha encontrado ninguna obra cuyo artista posea nacionalidad: {nacionalidad_string}\n")
                                     
                                    
                                    
                                         
                        #Punto c. del módulo de Búsqueda: 
                        if opcion_seleccionada == 2: 
                            encontrado_nombre = False
                            print("\nPor favor, indique si su artista posee uno o dos apellidos")
                            num_apellido = self.menu(opciones_apellidos)
                            
                            #Opción para un nombre y un apellido
                            if num_apellido == 0: 
                                nombre_artista = input("\nIndicar el nombre del artista cuyas obras desea buscar: ")
                                while not nombre_artista.isalpha(): 
                                    nombre_artista = input("\nPor favor, no introduzca valores numéricos o espacios en el nombre: ")
                                apellido_artista = input("\nIndicar el apellido del artista cuyas obras desea buscar: ")
                                while not apellido_artista.isalpha(): 
                                    apellido_artista = input("\nPor favor, no introduzca valores numéricos o espacios en el apellido: ")
                                nombre_completo_1 = nombre_artista.capitalize() + " " + apellido_artista.capitalize()
                                for obra in self.obras: 
                                    if nombre_completo_1 == obra.nombre_artista:
                                        encontrado_nombre = True
                                        #Se llama al método Show_busqueda de la clase obra
                                        obra.show_busqueda()
                                        print()
                                    else: 
                                        if encontrado_nombre == False and obra == self.obras[-1]: 
                                            print(f"\n No se ha encontrado ninguna obra cuyo artista posea el nombre de: {nombre_completo_1}\n")
                            else: #Opción para un nombre y dos apellidos
                                nombre_artista = input("\nIndicar el nombre del artista cuyas obras desea buscar: ")
                                while not nombre_artista.isalpha(): 
                                    nombre_artista = input("\nPor favor, no introduzca valores numéricos o espacios en el nombre: ")
                                apellido_1 = input("\nIndicar el primer apellido del artista cuyas obras desea buscar: ")
                                while not apellido_1.isalpha(): 
                                    apellido_1 = input("\nPor favor, no introduzca valores numéricos o espacios en el apellido: ")
                                apellido_2 = input("\nIndicar el segundo apellido del artista cuyas obras desea buscar: ")
                                while not apellido_2.isalpha(): 
                                    apellido_2 = input("\nPor favor, no introduzca valores numéricos o espacios en el apellido: ")
                                nombre_completo_2 = nombre_artista.capitalize() + " " + apellido_1.capitalize() + " " + apellido_2.capitalize()
                                for obra in self.obras: 
                                    if nombre_completo_2 == obra.nombre_artista: 
                                        #Se llama al método .Show_busqueda() de la clase Obra
                                        obra.show_busqueda()
                                        print() 
                                    else: 
                                        if encontrado_nombre == False and obra == self.obras[-1]: 
                                            print(f"\nNo se ha encontrado ninguna obra cuyo artista posea el nombre de: {nombre_completo_1}\n")

                        # Salida del módulo de Búsqueda
                        if opcion_seleccionada == 3: 
                            print()
                            break
                            
            
            #Módulo 3: Mostrar detalles de la obra
            if opcion_escogida == 2: 
                #Se verifica que existan obras cargadas para poder mostrar los detalles de alguna de las mismas
                if not self.obras: 
                    print("\nNo se encuentran obras guardadas actualmente, por favor elija un departamento de obras para poder iniciar la búsqueda\n")
                else:
                    obra_seleccionada = input("\nIndique el Id de la obra que desea escoger: ")
                    while not obra_seleccionada.isnumeric() or int(obra_seleccionada) not in self.lista_ids_obras: 
                        obra_seleccionada = input("\nError, por favor escoge una opción de Id válida: ")
                    nombre_archivo = "Imagen_aleatoria"
                    for obra in self.obras:
                        if int(obra_seleccionada) == obra.id_obra: 
                            obra_detallada = obra
                    #Se llama al método .show() de la clase Obra
                    obra_detallada.show()
                    print("\nDesea ver la imagen anexada a la obra?\n")
                    #Se genera un menú para decidir si se quiere visualizar la imagen por medio de la función self.menú(list)
                    ver_imagen = self.menu(self.opciones_binarias)
                    if ver_imagen == 0: 
                        #Se llama a la función guardar_imagen_desde_url(url,nombre_archivo)
                        imagen = self.guardar_imagen_desde_url(obra_detallada.imagen_obra, nombre_archivo)
                        img = Image.open(imagen) 
                        #Se llama la función .show() de la librería Pillow para mostrar la imagen
                        img.show()
                        print()
                    else: 
                        print("\nGracias por utilizar los servicios de búsqueda de MetroArt\n")

            # Salida del programa
            if opcion_escogida ==3: 
                print("\nGracias por visitar el museo vitural MetroArt\n")
                break

  
    def cargar_departamentos(self):  
        """
        Función para cargar los departamentos en una lista de objetos desde la API
        """
        depas = requests.get("https://collectionapi.metmuseum.org/public/collection/v1/departments")
        departamentos_dic = depas.json()["departments"]

        for departamento in departamentos_dic: 
            self.departamentos.append(Departamento(departamento["departmentId"], departamento["displayName"]))
            #Se cargan los Id de todos los departamentos en una lista aparte para ser utilizados en la verificación de la carga de departamentos
            self.lista_ids_departamentos.append(departamento["departmentId"])


    def cargar_obras(self, id_elegido): 
        """
        Función para cargar las obras en una lista de objetos desde la API
        """
        inicio_id = 0
        final_id = 20
        objetos = requests.get(f"https://collectionapi.metmuseum.org/public/collection/v1/objects?departmentIds={id_elegido}")
        obras_Id = objetos.json()["objectIDs"]
        #Se utilizan las variables inicio_id y final_id para seccionar la lista de obras_Id, tomar los primeros 20 elementos y guardarlos en las lista obras_Id_it
        obras_Id_it = obras_Id[inicio_id:final_id]


        for id in obras_Id_it:  
            obra = requests.get(f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{id}")
            
            try: 
                obra_dic = obra.json()
                print("\nCargando obras...\n")
                if not obra_dic["primaryImage"] == "": 
                    self.obras.append(Obra(obra_dic["title"], obra_dic["artistDisplayName"],obra_dic["artistNationality"], obra_dic["artistBeginDate"], obra_dic["artistEndDate"], obra_dic["classification"], obra_dic["objectDate"], obra_dic["primaryImage"], int(id_elegido), id))
                     #Se cargan los Id de todas las obras en una lista aparte para ser utilizados en la verificación de la carga de obras y en el módulo de mostrar detalles
                    self.lista_ids_obras.append(id)
                else: 
                    self.obras.append(Obra(obra_dic["title"], obra_dic["artistDisplayName"],obra_dic["artistNationality"], obra_dic["artistBeginDate"], obra_dic["artistEndDate"], obra_dic["classification"], obra_dic["objectDate"], "https://upload.wikimedia.org/wikipedia/commons/1/14/No_Image_Available.jpg", int(id_elegido), id))
                    #Se cargan los Id de todas las obras en una lista aparte para ser utilizados en la verificación de la carga de obras y en el módulo de mostrar detalles
                    self.lista_ids_obras.append(id)
            except ValueError: 
                print(f"{id} no valido")
            #Se pausa por 2 segundos la ejecución del programa para disminuir la velocidad de solicitudes a la API y lograr que no se bloquee el acceso a la información de la misma
            time.sleep(2)
            
        while True: 
            print("\nDesea continuar con la carga de datos? \n")
            continuar = self.menu(self.opciones_binarias)

            if continuar == 0: 
                inicio_id = final_id
                final_id = final_id + 20
                #Se utilizan inicio_id y final_id para seccionar la lista de obras_Id, tomar los siguientes 20 elementos y guardarlos en la lista obras_Id_it
                obras_Id_it = obras_Id[inicio_id:final_id]
                for id in obras_Id_it:  
                    obra = requests.get(f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{id}")
                    try: 
                        obra_dic = obra.json()
                        print("\nCargando obras...\n")
                        if not obra_dic["primaryImage"] == "": 
                            self.obras.append(Obra(obra_dic["title"], obra_dic["artistDisplayName"],obra_dic["artistNationality"], obra_dic["artistBeginDate"], obra_dic["artistEndDate"], obra_dic["classification"], obra_dic["objectDate"], obra_dic["primaryImage"], int(id_elegido), id))
                            #Se cargan los Id de todas las obras en una lista aparte para ser utilizados en la verificación de la carga de obras y en el módulo de mostrar detalles
                            self.lista_ids_obras.append(id)
                        else: 
                            self.obras.append(Obra(obra_dic["title"], obra_dic["artistDisplayName"],obra_dic["artistNationality"], obra_dic["artistBeginDate"], obra_dic["artistEndDate"], obra_dic["classification"], obra_dic["objectDate"], "https://upload.wikimedia.org/wikipedia/commons/1/14/No_Image_Available.jpg", int(id_elegido), id))
                            #Se cargan los Id de todas las obras en una lista aparte para ser utilizados en la verificación de la carga de obras y en el módulo de mostrar detalles
                            self.lista_ids_obras.append(id)
                    except ValueError: 
                        print(f"{id} no valido")
                         #Se pausa por 2 segundos la ejecución del programa para disminuir la velocidad de solicitudes a la API y lograr que no se bloquee el acceso a la información de la misma
                    time.sleep(2)
            if continuar == 1: 
                break
             

        
            print("Proceso culminado")

    def cargar_csv(self): 
       """
       Función para cargar el csv
       """
       df = pd.read_csv(r"C:\Users\Usuario\Desktop\CH_Nationality_List_20171130_v1.csv")
       self.lista_países = df["Nationality"].values.tolist()
       
    def guardar_imagen_desde_url(self, url, nombre_archivo):
        """
        Descarga una imagen desde una URL y la guarda en un archivo.
        """

    
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()  # Lanza una excepción para códigos de estado de error (4xx o 5xx)


            content_type = response.headers.get('Content-Type')
            extension = '.png'  # Valor por defecto
            if content_type:
                if 'image/png' in content_type:
                    extension = '.png'
                elif 'image/jpeg' in content_type:
                    extension = '.jpg'
                elif 'image/svg+xml' in content_type:
                    extension = '.svg'
        


            nombre_archivo_final = f"{nombre_archivo}{extension}"

             
            with open(nombre_archivo_final, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
            



        except requests.exceptions.RequestException as e:
            print(f"Error al hacer el request: {e}")
        except IOError as e:
            print(f"Error al escribir el archivo: {e}")
        return nombre_archivo_final
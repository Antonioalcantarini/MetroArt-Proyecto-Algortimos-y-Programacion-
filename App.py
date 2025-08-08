import requests
from Departamento import Departamento
from Obra import Obra
from PIL import Image
import pandas as pd
import time

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

        print("\n IMPORTANTE: no podrá realizar la busqueda de obras o mostrar detalles de las mismas sin haber elegido un departamento\n")

        while True: 
            opciones = ["Elegir departamento de obras", "Busqueda de obras", "Mostrar detalles de la obra", "Salir"]
            opciones_apellidos = ["Un apellido",  "Dos apellidos"]
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
                                         

                        if opcion_seleccionada == 2: 
                            print("Por favor, indique si su artista posee uno o dos apellidos")
                            num_apellido = self.menu(opciones_apellidos)
                            
                            if num_apellido == 0: 
                                nombre_artista = input("Indicar el nombre del artista cuyas obras desea buscar: ")
                                apellido_artista = input("Indicar el apellido del artista cuyas obras desea buscar: ")
                                nombre_completo_1 = nombre_artista + " " + apellido_artista
                                for obra in self.obras: 
                                    if nombre_completo_1 == obra.nombre_artista:
                                        obra.show_busqueda()
                                        print()
                            else: 
                                nombre_artista = input("Indicar el nombre del artista cuyas obras desea buscar: ")
                                apellido_1 = input("Indicar el primer apellido del artista cuyas obras desea buscar: ")
                                apellido_2 = input("Indicar el segundo apellido del artista cuyas obras desea buscar: ")
                                nombre_completo_2 = nombre_artista + " " + apellido_1 + " " + apellido_2
                                for obra in self.obras: 
                                    if nombre_completo_2 == obra.nombre_artista: 
                                        obra.show_busqueda()
                                        print() 

                        if opcion_seleccionada == 3: 
                            break

            if opcion_escogida == 2: 
                if not self.obras: 
                    print("\n No se encuentran obras guardadas actualmente, por favor elija un departamento de obras para poder iniciar la busqueda\n")
                else:
                    obra_seleccionada = input("Indique el Id de la obra que desea escoger: ")
                    while not obra_seleccionada.isnumeric(): 
                        obra_seleccionada = input("Error, por favor escoge una opción de Id válida: ")
                    nombre_archivo = "Imagen_aleatoria"
                    for obra in self.obras:
                        if int(obra_seleccionada) == obra.id_obra: 
                            obra_detallada = obra
                    imagen = self.guardar_imagen_desde_url(obra_detallada.imagen_obra, nombre_archivo)
                    img = Image.open(imagen)
                    obra_detallada.imagen_obra == img.show()
                    obra_detallada.show()


                

            if opcion_escogida ==3: 
                print("Gracias por visitar el museo vitural MetroArt")
                break

  
    def cargar_departamentos(self):  
        depas = requests.get("https://collectionapi.metmuseum.org/public/collection/v1/departments")
        departamentos_dic = depas.json()["departments"]

        for departamento in departamentos_dic: 
            self.departamentos.append(Departamento(departamento["departmentId"], departamento["displayName"]))
            self.lista_ids_departamentos.append(departamento["departmentId"])


    def cargar_obras(self, id_elegido): 
        inicio_id = 0
        final_id = 20
        objetos = requests.get(f"https://collectionapi.metmuseum.org/public/collection/v1/objects?departmentIds={id_elegido}")
        obras_Id = objetos.json()["objectIDs"]
        print(obras_Id)
        obras_Id_it = obras_Id[inicio_id:final_id]


        for id in obras_Id_it:  #departamento 3
            obra = requests.get(f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{id}")
            print(obra.text)
            try: 
                obra_dic = obra.json()
                if not obra_dic["primaryImage"] == "": 
                    self.obras.append(Obra(obra_dic["title"], obra_dic["artistDisplayName"],obra_dic["artistNationality"], obra_dic["artistBeginDate"], obra_dic["artistEndDate"], obra_dic["classification"], obra_dic["objectDate"], obra_dic["primaryImage"], int(id_elegido), id))
                else: 
                    self.obras.append(Obra(obra_dic["title"], obra_dic["artistDisplayName"],obra_dic["artistNationality"], obra_dic["artistBeginDate"], obra_dic["artistEndDate"], obra_dic["classification"], obra_dic["objectDate"], "https://upload.wikimedia.org/wikipedia/commons/1/14/No_Image_Available.jpg", int(id_elegido), id))
            except ValueError: 
                print(f"{id} no valido")
            time.sleep(2)
            
        while True: 
            continuar = input("Desea continuar la carga de datos? Si = 1, No = 2 ")

            if continuar == "1": 
                inicio_id = final_id
                print(inicio_id)
                final_id = final_id + 20 
                print(final_id)
                obras_Id_it = obras_Id[inicio_id:final_id]
                for id in obras_Id_it:  #departamento 3
                    obra = requests.get(f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{id}")
                    print(id)
                    print(obra.text)
                    try: 
                        obra_dic = obra.json()
                        self.obras.append(Obra(obra_dic["title"], obra_dic["artistDisplayName"],obra_dic["artistNationality"], obra_dic["artistBeginDate"], obra_dic["artistEndDate"], obra_dic["classification"], obra_dic["objectDate"], obra_dic["primaryImage"], int(self.Id_elegido), id))
                    except ValueError: 
                        print(f"{id} no valido")
                    time.sleep(2)
            else: 
                break
             

        
            print("Proceso culminado")

    def cargar_csv(self): 
       df = pd.read_csv(r"C:\Users\anton\Downloads\CH_Nationality_List_20171130_v1.csv")
       self.lista_países = df["Nationality"].values.tolist()
       
    def guardar_imagen_desde_url(self, url, nombre_archivo):
    
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

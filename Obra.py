class Obra:
    def __init__ (self, id, titulo, nombre_artista, nacionalidad_artista, fecha_nacimiento, fecha_muerte, tipo, ano_creacion, imagen_obra):
        self.id = id
        self.titulo = titulo
        self.nombre_artista = nombre_artista
        self.nacionalidad_artista = nacionalidad_artista
        self.fecha_nacimiento = fecha_nacimiento
        self.fecha_muerte = fecha_muerte
        self.tipo = tipo
        self.ano_creacion = ano_creacion
        self.imagen_obra = imagen_obra
    def show(self): 
        print(f"Título: {self.titulo}, Nombre del artista: {self.nombre_artista}, Nacionalidad del artista: {self.nacionalidad_artista}, Fecha de nacimiento: {self.fecha_nacimiento}, Fecha de muerte: {self.fecha_muerte}, Tipo: {self.tipo}, Año de creación: {self.ano_creacion}, Imagen de la obra: {self.imagen_obra} ")


class Departamento:
    def __init__(self, nombre, id, obras):
        self.nombre = nombre
        self.id = id
        self.obras = obras
        
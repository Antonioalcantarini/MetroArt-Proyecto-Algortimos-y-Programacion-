class Obra(): 
    def __init__(self, titulo, nombre_artista, nacionalidad_artista, fecha_nacimiento, fecha_muerte, tipo, año_creacion, imagen_obra, id_departamento, id_obra): 
        self.titulo = titulo
        self.nombre_artista = nombre_artista
        self.nacionalidad_artista = nacionalidad_artista
        self.fecha_nacimiento = fecha_nacimiento
        self.fecha_muerte = fecha_muerte
        self.tipo = tipo
        self.año_creacion = año_creacion
        self.imagen_obra = imagen_obra
        self.id_departamento = id_departamento
        self.id_obra = id_obra

    def show(self): 
        """
        Método para imprimir los atributos del objeto obra en el módulo 3: Mostrar detalles
        """
        print(f"Título: {self.titulo}, Nombre del artista: {self.nombre_artista}, Nacionalidad del artista: {self.nacionalidad_artista}, Fecha de nacimiento: {self.fecha_nacimiento}, Fecha de muerte: {self.fecha_muerte}, Tipo: {self.tipo}, Año de creación: {self.año_creacion}, Imagen de la obra: {self.imagen_obra}")

    def show_busqueda(self): 
        """
        Método para imprimir los atributos del objeto obra en el módulo 2: Búsqueda de obras
        """
        print(f"\n ID de la obra: {self.id_obra}, Título: {self.titulo}, Nombre del autor: {self.nombre_artista}")
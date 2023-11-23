from app_flask.config.mysqlconnection import connectToMySQL
from app_flask.modelos import modelo_usuarios
from flask import flash
from app_flask import BASE_DATOS

class Band:
    def __init__(self, datos):
        self.id = datos['id']
        self.name = datos['name']
        self.music = datos['music']
        self.city = datos['city']
        self.fecha_creacion = datos['fecha_creacion']
        self.fecha_actualizacion = datos['fecha_actualizacion']
        self.id_usuario = datos['id_usuario']
        self.usuario = None

    @classmethod
    def crear_uno(cls, datos):
        query = """
                INSERT INTO band (name, music, city, id_usuario)
                VALUES (%(name)s, %(music)s, %(city)s, %(id_usuario)s);
                """
        return connectToMySQL(BASE_DATOS).query_db(query, datos)

    @classmethod
    def obtener_todos(cls):
            query = """
                    SELECT * 
                    FROM band JOIN usuarios
                    ON band.id_usuario = usuarios.id;
                    """
            resultado = connectToMySQL(BASE_DATOS).query_db(query)
            lista_band = []
            for renglon in resultado:
                band_actual = cls(renglon)
                print(renglon)
                usuario = {
                    **renglon,
                    'nombre' : renglon['nombre'],
                    'id' : renglon['usuarios.id'],
                    'fecha_creacion' : renglon['fecha_creacion'],
                    'fecha_actualizacion' : renglon['fecha_actualizacion']
                }
                band_actual.usuario = modelo_usuarios.Usuario(usuario)
                lista_band.append(band_actual)
            return lista_band

    @classmethod
    def elimina_uno(cls, datos):
            query = """
                    DELETE FROM band 
                    WHERE id = %(id)s;
                    """
            return connectToMySQL(BASE_DATOS).query_db(query, datos)
    
    @classmethod
    def actualizar_uno(cls, datos):
        query = """
                UPDATE band 
                SET name = %(name)s, music = %(music)s, city = %(city)s,
                    id_usuario = %(id_usuario)s
                WHERE id = %(id)s;
                """
        return connectToMySQL(BASE_DATOS).query_db(query, datos)
    
    @classmethod
    def obtener_uno(cls, datos):
        query = """
                SELECT *
                FROM band
                WHERE id = %(id)s;
                """
        resultado = connectToMySQL(BASE_DATOS).query_db(query, datos)
        return cls(resultado[0])
    
    @classmethod
    def obtener_todos_con_usuario(cls, datos):
        query = """
                SELECT *
                FROM band 
                WHERE id_usuario = %(id_usuario)s;
                """
        resultados = connectToMySQL(BASE_DATOS).query_db(query, datos)
        bands = []
        for resultado in resultados:
            bands.append(cls(resultado))
        return bands
    
    @staticmethod
    def validar_band(datos):
        es_valido = True
        if len(datos['name']) < 2:
            flash('El nombre de la banda debe tener al menos 2 caracteres', 'error_name')
            es_valido = False
        if len(datos['music']) < 2:
            flash('El nombre del genero musical debe tener al menos 2 caracteres.', 'error_music')
            es_valido = False
        if len(datos['city']) < 2:
            flash('Por favor agregale una ciudad.', 'error_city')
            es_valido = False
        return es_valido
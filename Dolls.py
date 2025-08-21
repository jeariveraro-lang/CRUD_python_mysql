from Conexion import CConexion
from mysql.connector import Error

class CDolls:
    @staticmethod
    def crear(nombre, edad, activo=True):
        try:
            conexion = CConexion.ConexionBaseDeDatos()
            cursor = conexion.cursor()
            sql = "INSERT INTO dolls (nombre, edad, activo) VALUES (%s,%s,%s)"
            cursor.execute(sql, (nombre, edad, 1 if activo else 0))
            conexion.commit()
        except Error as e:
            print("Error al crear Doll:", e)
        finally:
            cursor.close()
            conexion.close()

    @staticmethod
    def listar():
        try:
            conexion = CConexion.ConexionBaseDeDatos()
            cursor = conexion.cursor(dictionary=True)
            sql = """SELECT d.*,
                            (SELECT COUNT(*) FROM cartas c 
                             WHERE c.doll_id=d.id AND c.estado IN ('borrador','revisado')) 
                             AS cartas_en_proceso
                     FROM dolls d"""
            cursor.execute(sql)
            return cursor.fetchall()
        except Error as e:
            print("Error al listar Dolls:", e)
            return []
        finally:
            cursor.close()
            conexion.close()

    @staticmethod
    def actualizar(id_, nombre, edad, activo):
        try:
            conexion = CConexion.ConexionBaseDeDatos()
            cursor = conexion.cursor()
            sql = "UPDATE dolls SET nombre=%s, edad=%s, activo=%s WHERE id=%s"
            cursor.execute(sql, (nombre, edad, 1 if activo else 0, id_))
            conexion.commit()
        except Error as e:
            print("Error al actualizar Doll:", e)
        finally:
            cursor.close()
            conexion.close()

    @staticmethod
    def eliminar(id_):
        try:
            conexion = CConexion.ConexionBaseDeDatos()
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM dolls WHERE id=%s", (id_,))
            conexion.commit()
        except Error as e:
            print("Error al eliminar Doll:", e)
        finally:
            cursor.close()
            conexion.close()

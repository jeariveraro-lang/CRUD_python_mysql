from Conexion import CConexion
from mysql.connector import Error

class CClientes:
    @staticmethod
    def crear(nombre, ciudad, motivo, contacto):
        try:
            conexion = CConexion.ConexionBaseDeDatos()
            cursor = conexion.cursor()
            sql = "INSERT INTO clientes (nombre, ciudad, motivo, contacto) VALUES (%s,%s,%s,%s)"
            cursor.execute(sql, (nombre, ciudad, motivo, contacto))
            conexion.commit()
        except Error as e:
            print("Error al crear cliente:", e)
        finally:
            cursor.close()
            conexion.close()

    @staticmethod
    def listar(busqueda=None, ciudad=None):
        try:
            conexion = CConexion.ConexionBaseDeDatos()
            cursor = conexion.cursor(dictionary=True)
            sql = "SELECT * FROM clientes"
            filtros = []
            valores = []
            if busqueda:
                filtros.append("nombre LIKE %s")
                valores.append("%" + busqueda + "%")
            if ciudad:
                filtros.append("ciudad LIKE %s")
                valores.append("%" + ciudad + "%")
            if filtros:
                sql += " WHERE " + " AND ".join(filtros)
            cursor.execute(sql, tuple(valores))
            return cursor.fetchall()
        except Error as e:
            print("Error al listar clientes:", e)
            return []
        finally:
            cursor.close()
            conexion.close()

    @staticmethod
    def obtener(id_):
        try:
            conexion = CConexion.ConexionBaseDeDatos()
            cursor = conexion.cursor(dictionary=True)
            cursor.execute("SELECT * FROM clientes WHERE id=%s", (id_,))
            return cursor.fetchone()
        except Error as e:
            print("Error al obtener cliente:", e)
        finally:
            cursor.close()
            conexion.close()

    @staticmethod
    def actualizar(id_, nombre, ciudad, motivo, contacto):
        try:
            conexion = CConexion.ConexionBaseDeDatos()
            cursor = conexion.cursor()
            sql = "UPDATE clientes SET nombre=%s, ciudad=%s, motivo=%s, contacto=%s WHERE id=%s"
            cursor.execute(sql, (nombre, ciudad, motivo, contacto, id_))
            conexion.commit()
        except Error as e:
            print("Error al actualizar cliente:", e)
        finally:
            cursor.close()
            conexion.close()

    @staticmethod
    def eliminar(id_):
        try:
            conexion = CConexion.ConexionBaseDeDatos()
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM clientes WHERE id=%s", (id_,))
            conexion.commit()
        except Error as e:
            print("Error al eliminar cliente:", e)
        finally:
            cursor.close()
            conexion.close()


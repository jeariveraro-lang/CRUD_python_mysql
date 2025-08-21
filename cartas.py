from Conexion import CConexion
from mysql.connector import Error

ESTADOS = ["borrador", "revisado", "enviado"]

class CCartas:
    @staticmethod
    def crear(cliente_id, doll_id, fecha, contenido, estado="borrador"):
        if not all([cliente_id, doll_id, fecha, contenido]):
            raise ValueError("Todos los campos son obligatorios")

        if CCartas._cartas_en_proceso(doll_id) >= 5 and estado in ("borrador", "revisado"):
            raise ValueError("La Doll seleccionada ya tiene 5 cartas en proceso")

        try:
            conexion = CConexion.ConexionBaseDeDatos()
            cursor = conexion.cursor()
            sql = """INSERT INTO cartas (cliente_id, doll_id, fecha, estado, contenido)
                     VALUES (%s, %s, %s, %s, %s)"""
            cursor.execute(sql, (cliente_id, doll_id, fecha, estado, contenido))
            conexion.commit()
        except Error as e:
            print("Error al crear carta:", e)
        finally:
            cursor.close()
            conexion.close()

    @staticmethod
    def listar(busqueda_cliente=None, ciudad=None):
        try:
            conexion = CConexion.ConexionBaseDeDatos()
            cursor = conexion.cursor(dictionary=True)
            sql = """SELECT c.id, cl.nombre AS cliente, cl.ciudad, d.nombre AS doll,
                            c.fecha, c.estado, c.contenido,
                            c.cliente_id, c.doll_id
                     FROM cartas c
                     JOIN clientes cl ON cl.id = c.cliente_id
                     JOIN dolls d ON d.id = c.doll_id"""
            filtros = []
            valores = []
            if busqueda_cliente:
                filtros.append("cl.nombre LIKE %s")
                valores.append("%" + busqueda_cliente + "%")
            if ciudad:
                filtros.append("cl.ciudad LIKE %s")
                valores.append("%" + ciudad + "%")
            if filtros:
                sql += " WHERE " + " AND ".join(filtros)
            sql += " ORDER BY c.id DESC"
            cursor.execute(sql, tuple(valores))
            return cursor.fetchall()
        except Error as e:
            print("Error al listar cartas:", e)
            return []
        finally:
            cursor.close()
            conexion.close()

    @staticmethod
    def obtener(id_):
        try:
            conexion = CConexion.ConexionBaseDeDatos()
            cursor = conexion.cursor(dictionary=True)
            cursor.execute("SELECT * FROM cartas WHERE id=%s", (id_,))
            return cursor.fetchone()
        except Error as e:
            print("Error al obtener carta:", e)
        finally:
            cursor.close()
            conexion.close()

    @staticmethod
    def actualizar(id_, cliente_id, doll_id, fecha, estado, contenido):
        actual = CCartas.obtener(id_)
        if not actual:
            raise ValueError("Carta no existe")

        # Validar flujo de estados
        allowed = {"borrador": "revisado", "revisado": "enviado", "enviado": None}
        if estado != actual["estado"]:
            if allowed.get(actual["estado"]) != estado:
                raise ValueError("Transición de estado inválida (solo borrador→revisado→enviado)")

        # Validar máximo de cartas en proceso
        if doll_id != actual["doll_id"] or estado in ("borrador","revisado"):
            if CCartas._cartas_en_proceso(doll_id) >= 5 and estado in ("borrador","revisado"):
                raise ValueError("La Doll seleccionada ya tiene 5 cartas en proceso")

        try:
            conexion = CConexion.ConexionBaseDeDatos()
            cursor = conexion.cursor()
            sql = """UPDATE cartas
                     SET cliente_id=%s, doll_id=%s, fecha=%s, estado=%s, contenido=%s
                     WHERE id=%s"""
            cursor.execute(sql, (cliente_id, doll_id, fecha, estado, contenido, id_))
            conexion.commit()
        except Error as e:
            print("Error al actualizar carta:", e)
        finally:
            cursor.close()
            conexion.close()

    @staticmethod
    def eliminar(id_):
        actual = CCartas.obtener(id_)
        if not actual:
            raise ValueError("Carta no existe")
        if actual["estado"] != "borrador":
            raise ValueError("Solo se pueden eliminar cartas en estado 'borrador'")

        try:
            conexion = CConexion.ConexionBaseDeDatos()
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM cartas WHERE id=%s", (id_,))
            conexion.commit()
        except Error as e:
            print("Error al eliminar carta:", e)
        finally:
            cursor.close()
            conexion.close()

    @staticmethod
    def _cartas_en_proceso(doll_id):
        try:
            conexion = CConexion.ConexionBaseDeDatos()
            cursor = conexion.cursor()
            cursor.execute("""SELECT COUNT(*) FROM cartas 
                              WHERE doll_id=%s AND estado IN ('borrador','revisado')""",
                           (doll_id,))
            return cursor.fetchone()[0]
        except Error as e:
            print("Error al contar cartas en proceso:", e)
            return 0
        finally:
            cursor.close()
            conexion.close()

    @staticmethod
    def sugerir_doll():
        try:
            conexion = CConexion.ConexionBaseDeDatos()
            cursor = conexion.cursor(dictionary=True)
            cursor.execute("""
                SELECT d.id, d.nombre,
                       (SELECT COUNT(*) FROM cartas c 
                        WHERE c.doll_id=d.id AND c.estado IN ('borrador','revisado')) as en_proceso
                FROM dolls d
                WHERE d.activo=1
                ORDER BY en_proceso ASC, d.id ASC
            """)
            rows = cursor.fetchall()
            for r in rows:
                if r["en_proceso"] < 5:
                    return r["id"], r["nombre"]
            return None
        except Error as e:
            print("Error al sugerir doll:", e)
            return None
        finally:
            cursor.close()
            conexion.close()

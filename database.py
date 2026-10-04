import sqlite3

DB = "inventario.db"

class Database:

    def conectar(self):
        con = sqlite3.connect(DB)
        con.row_factory = sqlite3.Row
        return con

    def iniciar(self):
        con = None
        try:
            con = self.conectar()
            con.execute("""
                CREATE TABLE IF NOT EXISTS productos (
                    id           TEXT PRIMARY KEY,
                    nombre       TEXT NOT NULL,
                    descripcion  TEXT,
                    categoria    TEXT,
                    precio       REAL,
                    cantidad     INTEGER,
                    stock_minimo INTEGER
                )
            """)
            con.execute("""
                CREATE TABLE IF NOT EXISTS movimientos (
                    id_mov      INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_producto TEXT,
                    tipo        TEXT,
                    cantidad    INTEGER,
                    fecha       DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            con.execute("""
                CREATE TABLE IF NOT EXISTS usuarios (
                    usuario  TEXT PRIMARY KEY,
                    password TEXT NOT NULL,
                    rol      TEXT NOT NULL
                )
            """)
            con.commit()
        except sqlite3.Error as e:
            print(f"[ERROR] No se pudo inicializar la base de datos: {e}")
            if con:
                con.rollback()
        finally:
            if con:
                con.close()
        self.sembrar_usuarios_default()

    def sembrar_usuarios_default(self):
        con = None
        try:
            con = self.conectar()
            cantidad = con.execute("SELECT COUNT(*) FROM usuarios").fetchone()[0]
            if cantidad == 0:
                defaults = [
                    ("gerente", "123", "Gerente"),
                    ("almacen", "123", "Almacen"),
                    ("admin",   "123", "Administrador")
                ]
                con.executemany("INSERT INTO usuarios VALUES (?,?,?)", defaults)
                con.commit()
        except sqlite3.Error as e:
            print(f"[ERROR] No se pudo sembrar usuarios por defecto: {e}")
            if con:
                con.rollback()
        finally:
            if con:
                con.close()

    def obtener_usuario(self, usuario):
        con = None
        try:
            con = self.conectar()
            fila = con.execute(
                "SELECT * FROM usuarios WHERE usuario = ?", (usuario,)
            ).fetchone()
            return dict(fila) if fila else None
        except sqlite3.Error as e:
            print(f"[ERROR] No se pudo obtener el usuario: {e}")
            return None
        finally:
            if con:
                con.close()

    def obtener_todos_usuarios(self):
        con = None
        try:
            con = self.conectar()
            filas = con.execute(
                "SELECT * FROM usuarios ORDER BY rol"
            ).fetchall()
            return [dict(f) for f in filas]
        except sqlite3.Error as e:
            print(f"[ERROR] No se pudo obtener usuarios: {e}")
            return []
        finally:
            if con:
                con.close()

    def insertar_usuario(self, u):
        con = None
        try:
            con = self.conectar()
            con.execute(
                "INSERT INTO usuarios (usuario, password, rol) VALUES (?,?,?)",
                (u["usuario"], u["password"], u["rol"])
            )
            con.commit()
            return True
        except sqlite3.Error as e:
            print(f"[ERROR] No se pudo insertar el usuario: {e}")
            if con:
                con.rollback()
            return False
        finally:
            if con:
                con.close()

    def eliminar_usuario(self, usuario):
        con = None
        try:
            con = self.conectar()
            con.execute("DELETE FROM usuarios WHERE usuario = ?", (usuario,))
            con.commit()
            return True
        except sqlite3.Error as e:
            print(f"[ERROR] No se pudo eliminar el usuario: {e}")
            if con:
                con.rollback()
            return False
        finally:
            if con:
                con.close()

    def obtener_uno(self, id_prod):
        con = None
        try:
            con = self.conectar()
            fila = con.execute(
                "SELECT * FROM productos WHERE id = ?", (id_prod,)
            ).fetchone()
            return dict(fila) if fila else None
        except sqlite3.Error as e:
            print(f"[ERROR] No se pudo obtener el producto: {e}")
            return None
        finally:
            if con:
                con.close()

    def obtener_todos(self):
        con = None
        try:
            con = self.conectar()
            filas = con.execute(
                "SELECT * FROM productos ORDER BY nombre"
            ).fetchall()
            return [dict(f) for f in filas]
        except sqlite3.Error as e:
            print(f"[ERROR] No se pudo obtener los productos: {e}")
            return []
        finally:
            if con:
                con.close()

    def buscar_nombre(self, texto):
        con = None
        try:
            con = self.conectar()
            filas = con.execute(
                "SELECT * FROM productos WHERE nombre LIKE ? ORDER BY nombre",
                (f"%{texto}%",)
            ).fetchall()
            return [dict(f) for f in filas]
        except sqlite3.Error as e:
            print(f"[ERROR] No se pudo buscar productos por nombre: {e}")
            return []
        finally:
            if con:
                con.close()

    def insertar(self, p):
        con = None
        try:
            con = self.conectar()
            con.execute(
                "INSERT INTO productos VALUES (?,?,?,?,?,?,?)",
                (p["id"], p["nombre"], p["descripcion"], p["categoria"],
                 p["precio"], p["cantidad"], p["stock_minimo"])
            )
            con.commit()
            return True
        except sqlite3.IntegrityError:
            print(f"[ERROR] El ID '{p['id']}' ya existe en la base de datos.")
            if con:
                con.rollback()
            return False
        except sqlite3.Error as e:
            print(f"[ERROR] No se pudo insertar el producto: {e}")
            if con:
                con.rollback()
            return False
        finally:
            if con:
                con.close()

    def actualizar(self, p):
        con = None
        try:
            con = self.conectar()
            con.execute(
                """UPDATE productos SET nombre=?, descripcion=?, categoria=?,
                   precio=?, cantidad=?, stock_minimo=? WHERE id=?""",
                (p["nombre"], p["descripcion"], p["categoria"],
                 p["precio"], p["cantidad"], p["stock_minimo"], p["id"])
            )
            con.commit()
            return True
        except sqlite3.Error as e:
            print(f"[ERROR] No se pudo actualizar el producto: {e}")
            if con:
                con.rollback()
            return False
        finally:
            if con:
                con.close()

    def eliminar(self, id_prod):
        con = None
        try:
            con = self.conectar()
            con.execute("DELETE FROM productos WHERE id = ?", (id_prod,))
            con.commit()
            return True
        except sqlite3.Error as e:
            print(f"[ERROR] No se pudo eliminar el producto: {e}")
            if con:
                con.rollback()
            return False
        finally:
            if con:
                con.close()

    def guardar_movimiento(self, id_prod, tipo, cantidad):
        con = None
        try:
            con = self.conectar()
            con.execute(
                "INSERT INTO movimientos (id_producto, tipo, cantidad) VALUES (?,?,?)",
                (id_prod, tipo, cantidad)
            )
            con.commit()
            return True
        except sqlite3.Error as e:
            print(f"[ERROR] No se pudo guardar el movimiento: {e}")
            if con:
                con.rollback()
            return False
        finally:
            if con:
                con.close()

    def obtener_movimientos(self):
        con = None
        try:
            con = self.conectar()
            filas = con.execute("""
                SELECT m.id_mov, m.id_producto, p.nombre, m.tipo, m.cantidad, m.fecha
                FROM movimientos m
                JOIN productos p ON m.id_producto = p.id
                ORDER BY m.fecha DESC LIMIT 15
            """).fetchall()
            return [dict(f) for f in filas]
        except sqlite3.Error as e:
            print(f"[ERROR] No se pudo obtener los movimientos: {e}")
            return []
        finally:
            if con:
                con.close()

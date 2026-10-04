import csv
import os
import tkinter as tk
from tkinter import simpledialog, messagebox
from database import Database
from estructura_datos import Pila, Cola, buscar_en_lista

class Inventario:

    def __init__(self):
        self.db     = Database()
        self.pila   = Pila()
        self.cola   = Cola()

    def _mostrar_texto(self, titulo, contenido):
        """Muestra textos largos o tablas en una ventana secundaria con fuente monoespaciada."""
        ventana = tk.Toplevel()
        ventana.title(titulo)
        ventana.geometry("750x400")
        
        txt = tk.Text(ventana, font=("Courier New", 10), wrap="none")
        txt.pack(fill="both", expand=True, padx=10, pady=10)
        txt.insert("1.0", contenido)
        txt.config(state="disabled")

    def registrar(self):
        id_p = simpledialog.askstring("Registrar Producto", "ID o código:")
        if not id_p or not id_p.strip():
            return
        id_p = id_p.strip()
        
        if self.db.obtener_uno(id_p):
            messagebox.showerror("Error", "Ese ID ya está registrado.")
            return
            
        nombre = simpledialog.askstring("Registrar Producto", "Nombre:")
        if nombre is None: return
        
        desc = simpledialog.askstring("Registrar Producto", "Descripción:")
        if desc is None: return
        
        cat = simpledialog.askstring("Registrar Producto", "Categoría (ej. Abarrotes, Limpieza):")
        if cat is None: return
        
        precio = simpledialog.askfloat("Registrar Producto", "Precio de venta ($):")
        if precio is None: return
        
        cant = simpledialog.askinteger("Registrar Producto", "Cantidad inicial en almacén:")
        if cant is None: return
        
        minimo = simpledialog.askinteger("Registrar Producto", "Stock mínimo (cuando hay muy poco):")
        if minimo is None: return

        if precio < 0 or cant < 0 or minimo < 0:
            messagebox.showerror("Error", "Los valores no pueden ser negativos.")
            return
            
        p = {"id": id_p, "nombre": nombre.strip(), "descripcion": desc.strip(),
             "categoria": cat.strip(), "precio": precio, "cantidad": cant, "stock_minimo": minimo}
        self.db.insertar(p)
        self.pila.push(f"Alta: {nombre.strip()} (ID: {id_p})")
        messagebox.showinfo("Éxito", "Producto guardado correctamente.")

    def consultar(self):
        todos = self.db.obtener_todos()
        if not todos:
            messagebox.showinfo("Inventario", "El inventario está vacío.")
            return
            
        texto = f"{'ID':<10} {'Nombre':<22} {'Categoría':<15} {'Precio':>9} {'Cant.':>6} {'Min.':>5}\n"
        texto += "-" * 72 + "\n"
        for p in todos:
            alerta = " << BAJO" if p["cantidad"] <= p["stock_minimo"] else ""
            texto += f"{p['id']:<10} {p['nombre']:<22} {p['categoria']:<15} ${p['precio']:>8.2f} {p['cantidad']:>6} {p['stock_minimo']:>5}{alerta}\n"
        texto += f"\nTotal: {len(todos)} producto(s)"
        
        self._mostrar_texto("Todos los Productos", texto)

    def buscar(self):
        op = simpledialog.askstring("Buscar", "1. Buscar por ID exacto\n2. Buscar por nombre\n\nElige una opción:")
        if op == "1":
            id_p = simpledialog.askstring("Buscar por ID", "ID:")
            if id_p:
                p = self.db.obtener_uno(id_p.strip())
                if p:
                    self._mostrar_detalle(p)
                else:
                    messagebox.showinfo("Buscar", "No se encontró ningún producto con ese ID.")

        elif op == "2":
            texto = simpledialog.askstring("Buscar por Nombre", "Nombre (o parte del nombre):")
            if texto:
                resultados = self.db.buscar_nombre(texto.strip())
                if not resultados:
                    messagebox.showinfo("Buscar", "No se encontraron productos.")
                    return
                exacto = buscar_en_lista(resultados, texto.strip())
                if exacto:
                    messagebox.showinfo("Coincidencia exacta", self._formatear_detalle(exacto))
                else:
                    res = f"Se encontraron {len(resultados)} producto(s):\n\n"
                    for p in resultados:
                        res += f"  {p['id']} | {p['nombre']} | ${p['precio']:.2f} | Cant: {p['cantidad']}\n"
                    self._mostrar_texto("Resultados de la Búsqueda", res)

    def _formatear_detalle(self, p):
        return (f"ID          : {p['id']}\n"
                f"Nombre      : {p['nombre']}\n"
                f"Descripción : {p['descripcion']}\n"
                f"Categoría   : {p['categoria']}\n"
                f"Precio      : ${p['precio']:.2f}\n"
                f"Cantidad    : {p['cantidad']}\n"
                f"Stock min.  : {p['stock_minimo']}")

    def _mostrar_detalle(self, p):
        messagebox.showinfo(f"Detalle de: {p['nombre']}", self._formatear_detalle(p))

    def modificar(self):
        id_p = simpledialog.askstring("Modificar", "ID del producto a modificar:")
        if not id_p: return
        p = self.db.obtener_uno(id_p.strip())
        if not p:
            messagebox.showerror("Error", "Producto no encontrado.")
            return
            
        messagebox.showinfo("Aviso", f"Editando: {p['nombre']}.\nDeja los campos en blanco para no cambiarlos.")

        n = simpledialog.askstring("Modificar", f"Nombre [{p['nombre']}]:")
        if n is None: return
        if n.strip(): p["nombre"] = n.strip()

        d = simpledialog.askstring("Modificar", f"Descripción [{p['descripcion']}]:")
        if d is None: return
        if d.strip(): p["descripcion"] = d.strip()

        c = simpledialog.askstring("Modificar", f"Categoría [{p['categoria']}]:")
        if c is None: return
        if c.strip(): p["categoria"] = c.strip()

        pr = simpledialog.askstring("Modificar", f"Precio [${p['precio']:.2f}]:")
        if pr is None: return
        if pr.strip():
            try:
                val = float(pr.strip())
                p["precio"] = val if val >= 0 else p["precio"]
            except ValueError:
                pass

        sm = simpledialog.askstring("Modificar", f"Stock mínimo [{p['stock_minimo']}]:")
        if sm is None: return
        if sm.strip():
            try:
                val = int(sm.strip())
                p["stock_minimo"] = val if val >= 0 else p["stock_minimo"]
            except ValueError:
                pass

        self.db.actualizar(p)
        self.pila.push(f"Modificación: {p['nombre']}")
        messagebox.showinfo("Éxito", "Cambios guardados.")

    def eliminar(self):
        id_p = simpledialog.askstring("Eliminar", "ID del producto a eliminar:")
        if not id_p: return
        p = self.db.obtener_uno(id_p.strip())
        if not p:
            messagebox.showerror("Error", "Producto no encontrado.")
            return
            
        if messagebox.askyesno("Confirmar", f"¿Seguro que quieres eliminar '{p['nombre']}'?"):
            self.db.eliminar(id_p.strip())
            self.pila.push(f"Baja: {p['nombre']}")
            messagebox.showinfo("Éxito", "Producto eliminado.")

    def entrada(self):
        id_p = simpledialog.askstring("Entrada", "ID del producto:")
        if not id_p: return
        p = self.db.obtener_uno(id_p.strip())
        if not p:
            messagebox.showerror("Error", "Producto no encontrado.")
            return
            
        cant = simpledialog.askinteger("Entrada", f"¿Cuántas unidades ingresan de '{p['nombre']}'?")
        if cant is None: return
        if cant <= 0:
            messagebox.showerror("Error", "La cantidad tiene que ser mayor a 0.")
            return
            
        p["cantidad"] += cant
        self.db.actualizar(p)
        self.db.guardar_movimiento(id_p.strip(), "ENTRADA", cant)
        self.pila.push(f"Entrada +{cant}: {p['nombre']}")
        messagebox.showinfo("Éxito", f"Entrada registrada.\nExistencia nueva: {p['cantidad']} unidades.")

    def salida(self):
        id_p = simpledialog.askstring("Salida", "ID del producto:")
        if not id_p: return
        p = self.db.obtener_uno(id_p.strip())
        if not p:
            messagebox.showerror("Error", "Producto no encontrado.")
            return
            
        cant = simpledialog.askinteger("Salida", f"¿Cuántas unidades salen de '{p['nombre']}'? (Hay {p['cantidad']})")
        if cant is None: return
        if cant <= 0:
            messagebox.showerror("Error", "La cantidad tiene que ser mayor a 0.")
            return
        if cant > p["cantidad"]:
            messagebox.showerror("Error", f"No hay suficiente stock.\nSolo hay {p['cantidad']} unidades.")
            return
            
        p["cantidad"] -= cant
        self.db.actualizar(p)
        self.db.guardar_movimiento(id_p.strip(), "SALIDA", cant)
        self.pila.push(f"Salida -{cant}: {p['nombre']}")
        
        msg = f"Salida registrada.\nExistencia nueva: {p['cantidad']} unidades."
        if p["cantidad"] <= p["stock_minimo"]:
            self.cola.encolar(id_p.strip())
            msg += f"\n\nAVISO: '{p['nombre']}' tiene poco stock.\nSe agregó a la cola de resurtido."
            messagebox.showwarning("Stock Bajo", msg)
        else:
            messagebox.showinfo("Éxito", msg)

    def stock_bajo(self):
        todos = self.db.obtener_todos()
        alertas = [p for p in todos if p["cantidad"] <= p["stock_minimo"]]
        if not alertas:
            messagebox.showinfo("Stock", "Todo está bien. Ningún producto tiene stock bajo.")
            return
            
        texto = f"Productos que necesitan resurtido ({len(alertas)}):\n\n"
        texto += f"{'ID':<10} {'Nombre':<22} {'Tiene':>7} {'Mínimo':>8}\n"
        texto += "-" * 50 + "\n"
        for p in alertas:
            texto += f"{p['id']:<10} {p['nombre']:<22} {p['cantidad']:>7} {p['stock_minimo']:>8}\n"
            self.cola.encolar(p["id"])
            
        self._mostrar_texto("Productos con Stock Bajo", texto)

    def reporte(self):
        todos = self.db.obtener_todos()
        if not todos:
            messagebox.showinfo("Reporte", "Sin datos en el inventario.")
            return
            
        total_prod  = len(todos)
        total_units = sum(p["cantidad"] for p in todos)
        valor_total = sum(p["cantidad"] * p["precio"] for p in todos)
        en_alerta   = sum(1 for p in todos if p["cantidad"] <= p["stock_minimo"])

        texto = "--- REPORTE DEL INVENTARIO ---\n\n"
        texto += f"  Productos registrados  : {total_prod}\n"
        texto += f"  Unidades totales       : {total_units}\n"
        texto += f"  Valor del inventario   : ${valor_total:.2f}\n"
        texto += f"  Productos en alerta    : {en_alerta}\n"
        texto += f"  Último mov. (pila)     : {self.pila.ver_cima() or 'Sin movimientos'}\n"
        texto += f"  En cola de resurtido   : {self.cola.tamanio()} producto(s)\n"

        movs = self.db.obtener_movimientos()
        if movs:
            texto += "\n--- ÚLTIMOS 15 MOVIMIENTOS ---\n\n"
            texto += f"{'#':<5} {'Nombre':<22} {'Tipo':<10} {'Cant':>5}  Fecha\n"
            texto += "-" * 60 + "\n"
            for m in movs:
                texto += f"{m['id_mov']:<5} {m['nombre']:<22} {m['tipo']:<10} {m['cantidad']:>5}  {m['fecha']}\n"

        self._mostrar_texto("Reporte General", texto)

    def ver_cola(self):
        if self.cola.esta_vacia():
            messagebox.showinfo("Cola", "No hay productos pendientes de resurtir.")
            return
            
        texto = f"Productos en cola ({self.cola.tamanio()}):\n\n"
        for i, id_p in enumerate(self.cola.elementos):
            p = self.db.obtener_uno(id_p)
            nombre = p["nombre"] if p else id_p
            texto += f"  {i+1}. {nombre} (ID: {id_p})\n"
            
        if messagebox.askyesno("Cola de Resurtido", texto + "\n\n¿Marcar el primero como atendido?"):
            atendido = self.cola.desencolar()
            p = self.db.obtener_uno(atendido)
            nombre = p['nombre'] if p else atendido
            messagebox.showinfo("Éxito", f"'{nombre}' fue removido de la cola.")

    def exportar_csv(self):
        todos = self.db.obtener_todos()
        if not todos:
            messagebox.showerror("Error", "No hay productos para exportar.")
            return
        archivo = "inventario_exportado.csv"
        campos = ["id", "nombre", "descripcion", "categoria", "precio", "cantidad", "stock_minimo"]
        with open(archivo, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=campos)
            w.writeheader()
            w.writerows(todos)
        messagebox.showinfo("Exportar", f"Exportado exitosamente a '{archivo}'\n({len(todos)} productos).")

    def importar_csv(self):
        archivo = simpledialog.askstring("Importar", "Nombre del archivo CSV:")
        if not archivo: return
        archivo = archivo.strip()
        
        if not os.path.exists(archivo):
            messagebox.showerror("Error", "El archivo no existe.")
            return
            
        agregados = 0
        omitidos  = 0
        errores   = 0
        with open(archivo, newline="", encoding="utf-8") as f:
            for numero_fila, fila in enumerate(csv.DictReader(f), start=2):
                if self.db.obtener_uno(fila.get("id", "").strip()):
                    omitidos += 1
                    continue
                try:
                    p = {
                        "id":          fila["id"].strip(),
                        "nombre":      fila["nombre"].strip(),
                        "descripcion": fila.get("descripcion", "").strip(),
                        "categoria":   fila.get("categoria", "").strip(),
                        "precio":      float(fila["precio"]),
                        "cantidad":    int(fila["cantidad"]),
                        "stock_minimo":int(fila["stock_minimo"])
                    }
                    if not p["id"] or not p["nombre"]:
                        raise ValueError("ID o nombre vacíos")
                    if p["precio"] < 0 or p["cantidad"] < 0 or p["stock_minimo"] < 0:
                        raise ValueError("Valores negativos")
                except (ValueError, KeyError):
                    errores += 1
                    continue
                self.db.insertar(p)
                agregados += 1
                
        messagebox.showinfo("Resumen de Importación", 
                            f"Importación terminada:\n\n"
                            f"• {agregados} agregados nuevos\n"
                            f"• {omitidos} omitidos (ID repetido)\n"
                            f"• {errores} ignorados por errores de formato")

    def gestionar_usuarios(self):
        op = simpledialog.askstring("Usuarios", "1. Ver todos los usuarios\n2. Dar de alta un usuario\n3. Eliminar un usuario\n\nElige una opción:")
        
        if op == "1":
            usuarios = self.db.obtener_todos_usuarios()
            if not usuarios:
                messagebox.showinfo("Usuarios", "No hay usuarios registrados.")
            else:
                texto = f"{'Usuario':<15} {'Rol':<20}\n"
                texto += "-" * 35 + "\n"
                for u in usuarios:
                    texto += f"{u['usuario']:<15} {u['rol']:<20}\n"
                self._mostrar_texto("Usuarios del Sistema", texto)
                
        elif op == "2":
            nuevo = simpledialog.askstring("Nuevo Usuario", "Nombre de usuario:")
            if not nuevo or not nuevo.strip(): return
            nuevo = nuevo.strip()
            
            if self.db.obtener_usuario(nuevo):
                messagebox.showerror("Error", "Ese usuario ya existe.")
                return
                
            password = simpledialog.askstring("Nuevo Usuario", "Contraseña:")
            if not password or not password.strip(): return
            
            op_rol = simpledialog.askstring("Rol", "1. Gerente\n2. Almacen\n3. Administrador\n\nElige el rol:")
            rol = "Administrador" # Default
            if op_rol == "1": rol = "Gerente"
            elif op_rol == "2": rol = "Almacen"
            
            self.db.insertar_usuario({"usuario": nuevo, "password": password.strip(), "rol": rol})
            messagebox.showinfo("Éxito", f"Usuario '{nuevo}' creado con rol {rol}.")
            
        elif op == "3":
            usuario = simpledialog.askstring("Eliminar", "Nombre del usuario a eliminar:")
            if not usuario: return
            usuario = usuario.strip()
            
            if usuario in ("gerente", "almacen", "admin"):
                messagebox.showerror("Error", "No se pueden eliminar los usuarios predeterminados del sistema.")
                return
            if not self.db.obtener_usuario(usuario):
                messagebox.showerror("Error", "Ese usuario no existe.")
                return
                
            if messagebox.askyesno("Confirmar", f"¿Eliminar al usuario '{usuario}'?"):
                self.db.eliminar_usuario(usuario)
                messagebox.showinfo("Éxito", "Usuario eliminado.")
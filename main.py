import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import os
import sys
from database import Database
from inventario import Inventario

def obtener_ruta_recurso(ruta_relativa):
    """Encuentra la ruta absoluta correcta tanto si es un .py como un .exe"""
    try:
     
        ruta_base = sys._MEIPASS
    except Exception:
     
        ruta_base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(ruta_base, ruta_relativa)

class AplicacionAbarrotes(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Control de inventario- Lobos corporation")
        self.geometry("1024x720")
        
       
        ruta_logo = obtener_ruta_recurso("logo.ico")
        try:
            self.iconbitmap(ruta_logo)
        except Exception as e:
            print(f"⚠️ Aviso: No se pudo cargar el ícono. Verificando en: {ruta_logo}")
            print(f"Error técnico: {e}")
        
        # --- PALETA DE COLORES ---
        self.BG_COLOR = "#1ABC9C"  # Verde turquesa
        self.FG_COLOR = "black"    # Letras negras
        self.BTN_BG = "white"      # Botones blancos
        
        self.configure(bg=self.BG_COLOR)

       
        self.estilo = ttk.Style()
        self.estilo.theme_use('clam')
        
        self.estilo.configure("TButton", font=("Helvetica", 10), padding=5, background=self.BTN_BG, foreground=self.FG_COLOR)
        self.estilo.configure("Header.TButton", font=("Helvetica", 10, "bold"), background=self.BTN_BG, foreground=self.FG_COLOR)
        self.estilo.configure("Treeview.Heading", font=("Helvetica", 10, "bold"), background=self.BTN_BG, foreground=self.FG_COLOR)
        self.estilo.configure("Treeview", font=("Helvetica", 11), rowheight=30, background="white", foreground=self.FG_COLOR)
        
     
        self.db = Database()
        self.db.iniciar()
        self.inv = Inventario()

        self.frame_actual = None
        self.mostrar_login()

    def cambiar_frame(self, nuevo_frame):
        if self.frame_actual is not None:
            self.frame_actual.destroy()
        self.frame_actual = nuevo_frame
        self.frame_actual.pack(fill="both", expand=True)

   
    def mostrar_login(self):
        frame = tk.Frame(self, bg=self.BG_COLOR)
        tarjeta = tk.Frame(frame, bg="white", padx=60, pady=50, relief="ridge", bd=2)
        tarjeta.place(relx=0.5, rely=0.5, anchor="center") 
        
        tk.Label(tarjeta, text="INICIO DE SESIÓN", font=("Helvetica", 24, "bold"), bg="white", fg=self.FG_COLOR).pack(pady=(0, 30))
        
        tk.Label(tarjeta, text="Usuario:", font=("Helvetica", 12, "bold"), bg="white", fg=self.FG_COLOR).pack()
        self.entry_usuario = ttk.Entry(tarjeta, font=("Helvetica", 12), width=30)
        self.entry_usuario.pack(pady=(0, 15))

        tk.Label(tarjeta, text="Contraseña:", font=("Helvetica", 12, "bold"), bg="white", fg=self.FG_COLOR).pack()
        self.entry_password = ttk.Entry(tarjeta, font=("Helvetica", 12), width=30, show="*")
        self.entry_password.pack(pady=(0, 25))

        ttk.Button(tarjeta, text="Entrar al Sistema", command=self.iniciar_sesion).pack(pady=10, ipadx=10, ipady=5)
        
        tk.Label(tarjeta, text="¿No tienes cuenta?", font=("Helvetica", 10), bg="white", fg="#777").pack(pady=(20, 5))
        ttk.Button(tarjeta, text="Crear nueva cuenta", command=self.mostrar_registro).pack()

        self.cambiar_frame(frame)

    def iniciar_sesion(self):
        usuario = self.entry_usuario.get().strip()
        password = self.entry_password.get().strip()

        u = self.db.obtener_usuario(usuario)
        if u and u["password"] == password:
            self.mostrar_almacen(u["rol"], usuario)
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos.")

    def mostrar_registro(self):
        frame = tk.Frame(self, bg=self.BG_COLOR)
        tarjeta = tk.Frame(frame, bg="white", padx=60, pady=40, relief="ridge", bd=2)
        tarjeta.place(relx=0.5, rely=0.5, anchor="center")
        
        tk.Label(tarjeta, text="NUEVO REGISTRO", font=("Helvetica", 24, "bold"), bg="white", fg=self.FG_COLOR).pack(pady=(0, 30))
        
        tk.Label(tarjeta, text="Nombre de Usuario:", font=("Helvetica", 12, "bold"), bg="white", fg=self.FG_COLOR).pack()
        self.reg_usuario = ttk.Entry(tarjeta, font=("Helvetica", 12), width=30)
        self.reg_usuario.pack(pady=(0, 15))

        tk.Label(tarjeta, text="Contraseña:", font=("Helvetica", 12, "bold"), bg="white", fg=self.FG_COLOR).pack()
        self.reg_password = ttk.Entry(tarjeta, font=("Helvetica", 12), width=30, show="*")
        self.reg_password.pack(pady=(0, 15))

        tk.Label(tarjeta, text="Confirmar Contraseña:", font=("Helvetica", 12, "bold"), bg="white", fg=self.FG_COLOR).pack()
        self.reg_password_conf = ttk.Entry(tarjeta, font=("Helvetica", 12), width=30, show="*")
        self.reg_password_conf.pack(pady=(0, 15))

        tk.Label(tarjeta, text="Rol del Empleado:", font=("Helvetica", 12, "bold"), bg="white", fg=self.FG_COLOR).pack()
        self.reg_rol = ttk.Combobox(tarjeta, font=("Helvetica", 12), width=28, state="readonly")
        self.reg_rol['values'] = ("Gerente", "Almacen", "Administrador")
        self.reg_rol.current(1)
        self.reg_rol.pack(pady=(0, 25))

        ttk.Button(tarjeta, text="Registrar Usuario", command=self.guardar_nuevo_usuario).pack(pady=10, ipadx=10, ipady=2)
        ttk.Button(tarjeta, text="Volver al Login", command=self.mostrar_login).pack()

        self.cambiar_frame(frame)

    def guardar_nuevo_usuario(self):
        usuario = self.reg_usuario.get().strip()
        password = self.reg_password.get().strip()
        conf_password = self.reg_password_conf.get().strip()
        rol = self.reg_rol.get()

        if not usuario or not password:
            messagebox.showwarning("Atención", "El usuario y la contraseña no pueden estar vacíos.")
            return
            
        if password != conf_password:
            messagebox.showerror("Error", "Las contraseñas no coinciden. Intenta de nuevo.")
            return

        if self.db.obtener_usuario(usuario):
            messagebox.showerror("Error", "Ese nombre de usuario ya existe.")
            return

        self.db.insertar_usuario({"usuario": usuario, "password": password, "rol": rol})
        messagebox.showinfo("Registro Exitoso", f"El usuario '{usuario}' se ha creado correctamente.\nYa puedes iniciar sesión.")
        self.mostrar_login()

   
    def ventana_catalogo(self):
        ventana = tk.Toplevel(self)
        ventana.title("Catálogo de Productos")
        ventana.geometry("850x600")
        ventana.configure(bg=self.BG_COLOR)
        ventana.transient(self)
        ventana.grab_set()

        try:
            ventana.iconbitmap(obtener_ruta_recurso("logo.ico"))
        except Exception:
            pass

        tarjeta = tk.Frame(ventana, bg="white", padx=15, pady=15, relief="ridge", bd=2)
        tarjeta.pack(fill="both", expand=True, padx=20, pady=20)

        tk.Label(tarjeta, text="📦 CATÁLOGO COMPLETO DE PRODUCTOS", font=("Helvetica", 14, "bold"), bg="white", fg=self.FG_COLOR).pack(anchor="w", pady=(0, 5))
        tk.Label(tarjeta, text="Haz clic en la casilla [ ] para seleccionar los productos que deseas borrar.", font=("Helvetica", 10), bg="white", fg="#7f8c8d").pack(anchor="w", pady=(0, 15))

        frame_tabla = tk.Frame(tarjeta)
        frame_tabla.pack(fill="both", expand=True)

        columnas = ("check", "id", "nombre", "categoria", "precio", "stock", "minimo")
        tree = ttk.Treeview(frame_tabla, columns=columnas, show="headings", selectmode="none")
        
        tree.heading("check", text="✔")
        tree.heading("id", text="Código")
        tree.heading("nombre", text="Nombre del Producto")
        tree.heading("categoria", text="Categoría")
        tree.heading("precio", text="Precio")
        tree.heading("stock", text="Stock Actual")
        tree.heading("minimo", text="Mínimo")

        tree.column("check", width=40, anchor="center")
        tree.column("id", width=80, anchor="center")
        tree.column("nombre", width=250, anchor="w")
        tree.column("categoria", width=120, anchor="center")
        tree.column("precio", width=90, anchor="center")
        tree.column("stock", width=90, anchor="center")
        tree.column("minimo", width=90, anchor="center")

        tree.tag_configure("BAJO", foreground="#c0392b", background="#fdedec")

        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        todos = self.db.obtener_todos()
        if todos:
            for p in todos:
                tag = "BAJO" if p["cantidad"] <= p["stock_minimo"] else "NORMAL"
                tree.insert("", "end", values=("☐", p['id'], p['nombre'], p['categoria'], f"${p['precio']:.2f}", p['cantidad'], p['stock_minimo']), tags=(tag,))
        else:
            messagebox.showinfo("Inventario Vacío", "No hay productos registrados en el sistema.", parent=ventana)

        def toggle_check(event):
            region = tree.identify("region", event.x, event.y)
            if region == "cell":
                columna = tree.identify_column(event.x)
                if columna == "#1":  
                    item = tree.identify_row(event.y)
                    if item:
                        valores = list(tree.item(item, "values"))
                        if valores[0] == "☐":
                            valores[0] = "☑"
                        else:
                            valores[0] = "☐"
                        tree.item(item, values=valores)

        tree.bind("<ButtonRelease-1>", toggle_check)

        def eliminar_seleccionados():
            a_borrar = []
            nombres_a_borrar = []
            
            for item in tree.get_children():
                valores = tree.item(item, "values")
                if valores[0] == "☑":
                    a_borrar.append(item)
                    nombres_a_borrar.append(valores[2])

            if not a_borrar:
                messagebox.showwarning("Atención", "No has marcado ninguna casilla.\nHaz clic en las casillas [ ] de la primera columna para seleccionar productos.", parent=ventana)
                return
            
            cantidad = len(a_borrar)
            
            if cantidad == 1:
                mensaje = f"¿Estás seguro de que deseas eliminar '{nombres_a_borrar[0]}' de forma permanente?"
            else:
                mensaje = f"¿Estás seguro de que deseas eliminar estos {cantidad} productos seleccionados de forma permanente?"

            confirmacion = messagebox.askyesno("Confirmar Eliminación", mensaje, parent=ventana)
            
            if confirmacion:
                for item in a_borrar:
                    valores = tree.item(item, "values")
                    id_p = valores[1]
                    nombre_p = valores[2]
                    
                    self.db.eliminar(id_p)                  
                    tree.delete(item)                       
                    self.inv.pila.push(f"Baja: {nombre_p}") 
                
                messagebox.showinfo("Éxito", f"Se eliminaron {cantidad} producto(s) correctamente.", parent=ventana)

        frame_botones = tk.Frame(tarjeta, bg="white")
        frame_botones.pack(fill="x", pady=(15, 0))
        
        btn_eliminar = tk.Button(frame_botones, text="🗑️ Eliminar Seleccionados", font=("Helvetica", 11, "bold"), bg="#c0392b", fg="white", relief="flat", cursor="hand2", command=eliminar_seleccionados)
        btn_eliminar.pack(side="right", ipadx=15, ipady=6)

    def ventana_stock_bajo(self):
        ventana = tk.Toplevel(self)
        ventana.title("Alerta de Stock Bajo")
        ventana.geometry("750x450")
        ventana.configure(bg=self.BG_COLOR)
        ventana.transient(self)
        ventana.grab_set()

        try:
            ventana.iconbitmap(obtener_ruta_recurso("logo.ico"))
        except:
            pass

        tarjeta = tk.Frame(ventana, bg="white", padx=15, pady=15, relief="ridge", bd=2)
        tarjeta.pack(fill="both", expand=True, padx=20, pady=20)

        tk.Label(tarjeta, text="⚠️ PRODUCTOS QUE NECESITAN RESURTIDO", font=("Helvetica", 14, "bold"), bg="white", fg="#c0392b").pack(anchor="w", pady=(0, 15))

        columnas = ("id", "nombre", "stock", "minimo", "faltante")
        tree = ttk.Treeview(tarjeta, columns=columnas, show="headings", selectmode="extended")
        
        tree.heading("id", text="Código")
        tree.heading("nombre", text="Nombre del Producto")
        tree.heading("stock", text="Stock Actual")
        tree.heading("minimo", text="Mínimo Requerido")
        tree.heading("faltante", text="Para llegar al mín.")

        tree.column("id", width=80, anchor="center")
        tree.column("nombre", width=300, anchor="w")
        tree.column("stock", width=100, anchor="center")
        tree.column("minimo", width=120, anchor="center")
        tree.column("faltante", width=100, anchor="center")

        tree.tag_configure("PELIGRO", foreground="#c0392b", background="#fdedec")

        scrollbar = ttk.Scrollbar(tarjeta, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        todos = self.db.obtener_todos()
        alertas = [p for p in todos if p["cantidad"] <= p["stock_minimo"]]
        
        if alertas:
            for p in alertas:
                faltante = p["stock_minimo"] - p["cantidad"]
                self.inv.cola.encolar(p["id"])
                tree.insert("", "end", values=(p['id'], p['nombre'], p['cantidad'], p['stock_minimo'], f"+{faltante}"), tags=("PELIGRO",))
        else:
            messagebox.showinfo("Todo en orden", "No hay ningún producto con stock bajo en este momento.", parent=ventana)
            ventana.destroy()

    def ventana_nuevo_producto(self):
        ventana = tk.Toplevel(self)
        ventana.title("Registrar Nuevo Producto")
        ventana.geometry("450x600")
        ventana.configure(bg=self.BG_COLOR)
        ventana.transient(self) 
        ventana.grab_set()      

        try:
            ventana.iconbitmap(obtener_ruta_recurso("logo.ico"))
        except:
            pass

        tarjeta = tk.Frame(ventana, bg="white", padx=30, pady=20, relief="ridge", bd=2)
        tarjeta.pack(fill="both", expand=True, padx=20, pady=20)

        tk.Label(tarjeta, text="NUEVO PRODUCTO", font=("Helvetica", 16, "bold"), bg="white", fg=self.FG_COLOR).pack(pady=(0, 15))

        campos = [
            ("Código / ID:", "entry_id"),
            ("Nombre:", "entry_nombre"),
            ("Descripción:", "entry_desc"),
            ("Categoría:", "entry_cat"),
            ("Precio de Venta ($):", "entry_precio"),
            ("Cantidad Inicial:", "entry_cant"),
            ("Stock Mínimo de Alerta:", "entry_min")
        ]

        entradas = {}
        for texto, nombre_var in campos:
            frame_campo = tk.Frame(tarjeta, bg="white")
            frame_campo.pack(fill="x", pady=5)
            tk.Label(frame_campo, text=texto, font=("Helvetica", 10, "bold"), bg="white", width=18, anchor="e").pack(side="left", padx=(0,10))
            entry = ttk.Entry(frame_campo, font=("Helvetica", 11), width=20)
            entry.pack(side="left")
            entradas[nombre_var] = entry

        def guardar():
            id_p = entradas["entry_id"].get().strip()
            nombre = entradas["entry_nombre"].get().strip()
            
            if not id_p or not nombre:
                messagebox.showwarning("Atención", "El Código y el Nombre son obligatorios.", parent=ventana)
                return
                
            if self.db.obtener_uno(id_p):
                messagebox.showerror("Error", "Ese Código/ID ya está registrado.", parent=ventana)
                return

            try:
                precio = float(entradas["entry_precio"].get().strip() or 0)
                cant = int(entradas["entry_cant"].get().strip() or 0)
                minimo = int(entradas["entry_min"].get().strip() or 0)
                if precio < 0 or cant < 0 or minimo < 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Error", "El precio y las cantidades deben ser números positivos válidos.", parent=ventana)
                return

            p = {
                "id": id_p, 
                "nombre": nombre, 
                "descripcion": entradas["entry_desc"].get().strip(),
                "categoria": entradas["entry_cat"].get().strip(), 
                "precio": precio, 
                "cantidad": cant, 
                "stock_minimo": minimo
            }
            
            self.db.insertar(p)
            self.inv.pila.push(f"Alta: {nombre} (ID: {id_p})")
            messagebox.showinfo("Éxito", "Producto guardado correctamente en la base de datos.", parent=ventana)
            ventana.destroy()

        ttk.Button(tarjeta, text="💾 Guardar Producto", command=guardar, style="Header.TButton").pack(pady=20, ipadx=10, ipady=5)

    def ventana_buscar_producto(self):
        ventana = tk.Toplevel(self)
        ventana.title("Buscador de Productos")
        ventana.geometry("700x450")
        ventana.configure(bg=self.BG_COLOR)
        ventana.transient(self)
        ventana.grab_set()

        try:
            ventana.iconbitmap(obtener_ruta_recurso("logo.ico"))
        except:
            pass

        tarjeta = tk.Frame(ventana, bg="white", padx=20, pady=20)
        tarjeta.pack(fill="both", expand=True, padx=15, pady=15)

        top_frame = tk.Frame(tarjeta, bg="white")
        top_frame.pack(fill="x", pady=(0, 15))
        
        tk.Label(top_frame, text="Buscar:", font=("Helvetica", 12, "bold"), bg="white").pack(side="left", padx=(0,10))
        entry_busqueda = ttk.Entry(top_frame, font=("Helvetica", 12), width=40)
        entry_busqueda.pack(side="left", padx=5)

        columnas = ("id", "nombre", "categoria", "precio", "stock")
        tree_resultados = ttk.Treeview(tarjeta, columns=columnas, show="headings", height=10)
        
        tree_resultados.heading("id", text="Código")
        tree_resultados.heading("nombre", text="Nombre")
        tree_resultados.heading("categoria", text="Categoría")
        tree_resultados.heading("precio", text="Precio")
        tree_resultados.heading("stock", text="Stock")

        tree_resultados.column("id", width=80, anchor="center")
        tree_resultados.column("nombre", width=250, anchor="w")
        tree.column("categoria", width=120, anchor="center")
        tree_resultados.column("precio", width=80, anchor="center")
        tree_resultados.column("stock", width=60, anchor="center")

        scrollbar = ttk.Scrollbar(tarjeta, orient="vertical", command=tree_resultados.yview)
        tree_resultados.configure(yscrollcommand=scrollbar.set)
        
        tree_resultados.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        def realizar_busqueda(event=None):
            for item in tree_resultados.get_children():
                tree_resultados.delete(item)
                
            texto = entry_busqueda.get().strip()
            if not texto:
                resultados = self.db.obtener_todos()
            else:
                p = self.db.obtener_uno(texto)
                if p:
                    resultados = [p]
                else:
                    resultados = self.db.buscar_nombre(texto)

            if resultados:
                for p in resultados:
                    tree_resultados.insert("", "end", values=(p['id'], p['nombre'], p['categoria'], f"${p['precio']:.2f}", p['cantidad']))
            else:
                messagebox.showinfo("Sin resultados", "No se encontró ningún producto con ese criterio.", parent=ventana)

        ttk.Button(top_frame, text="🔍 Buscar", command=realizar_busqueda, style="Header.TButton").pack(side="left", padx=10)
        entry_busqueda.bind("<Return>", realizar_busqueda)
        realizar_busqueda()

    def ventana_reporte(self):
        ventana = tk.Toplevel(self)
        ventana.title("Reporte General de Inventario")
        ventana.geometry("850x600")
        ventana.configure(bg=self.BG_COLOR)
        ventana.transient(self)
        ventana.grab_set()

        try:
            ventana.iconbitmap(obtener_ruta_recurso("logo.ico"))
        except:
            pass

        todos = self.db.obtener_todos()
        total_prod = len(todos)
        total_units = sum(p["cantidad"] for p in todos)
        valor_total = sum(p["cantidad"] * p["precio"] for p in todos)
        en_alerta = sum(1 for p in todos if p["cantidad"] <= p["stock_minimo"])

        frame_resumen = tk.Frame(ventana, bg="white", padx=20, pady=15, relief="ridge", bd=2)
        frame_resumen.pack(fill="x", padx=15, pady=15)
        
        tk.Label(frame_resumen, text="📊 DASHBOARD DE INVENTARIO", font=("Helvetica", 14, "bold"), bg="white", fg=self.FG_COLOR).pack(pady=(0, 15))

        grid_frame = tk.Frame(frame_resumen, bg="white")
        grid_frame.pack(fill="x")
        
        grid_frame.columnconfigure(0, weight=1)
        grid_frame.columnconfigure(1, weight=1)
        grid_frame.columnconfigure(2, weight=1)
        grid_frame.columnconfigure(3, weight=1)

        def crear_tarjeta(parent, titulo, valor, color, col):
            f = tk.Frame(parent, bg="white")
            f.grid(row=0, column=col, sticky="ew")
            tk.Label(f, text=titulo, font=("Helvetica", 11), bg="white", fg="#555").pack()
            tk.Label(f, text=valor, font=("Helvetica", 20, "bold"), bg="white", fg=color).pack()

        crear_tarjeta(grid_frame, "Productos Registrados", str(total_prod), "#2980b9", 0)
        crear_tarjeta(grid_frame, "Unidades en Almacén", str(total_units), "#27ae60", 1)
        crear_tarjeta(grid_frame, "Valor Total Estimado", f"${valor_total:,.2f}", "#8e44ad", 2)
        crear_tarjeta(grid_frame, "Productos en Alerta", str(en_alerta), "#c0392b", 3)

        frame_tabla = tk.Frame(ventana, bg="white", padx=15, pady=15, relief="ridge", bd=2)
        frame_tabla.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        tk.Label(frame_tabla, text="📋 HISTORIAL DE MOVIMIENTOS", font=("Helvetica", 12, "bold"), bg="white", fg=self.FG_COLOR).pack(anchor="w", pady=(0, 10))

        columnas = ("id_mov", "nombre", "tipo", "cantidad", "fecha")
        tree = ttk.Treeview(frame_tabla, columns=columnas, show="headings", selectmode="extended")
        
        tree.heading("id_mov", text="ID Mov.")
        tree.heading("nombre", text="Producto")
        tree.heading("tipo", text="Operación")
        tree.heading("cantidad", text="Cantidad")
        tree.heading("fecha", text="Fecha y Hora")

        tree.column("id_mov", width=70, anchor="center")
        tree.column("nombre", width=300, anchor="w")
        tree.column("tipo", width=100, anchor="center")
        tree.column("cantidad", width=80, anchor="center")
        tree.column("fecha", width=150, anchor="center")

        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        movs = self.db.obtener_movimientos()
        if movs:
            for m in movs:
                tree.insert("", "end", values=(m['id_mov'], m['nombre'], m['tipo'], m['cantidad'], m['fecha']))

 
   
    def mostrar_almacen(self, rol, nombre_usuario):
        frame = tk.Frame(self, bg=self.BG_COLOR)

        top_nav = tk.Frame(frame, bg=self.BG_COLOR, bd=1, relief="solid")
        top_nav.pack(fill="x", side="top")

        ttk.Button(top_nav, text="📦 Catálogo de Productos", style="Header.TButton", command=self.ventana_catalogo).pack(side="left", padx=2, pady=2)
        ttk.Button(top_nav, text="➕ Nuevo Producto", style="Header.TButton", command=self.ventana_nuevo_producto).pack(side="left", padx=2, pady=2)
        ttk.Button(top_nav, text="📊 Reporte General", style="Header.TButton", command=self.ventana_reporte).pack(side="left", padx=2, pady=2)
        ttk.Button(top_nav, text="⚠️ Stock Bajo", style="Header.TButton", command=self.ventana_stock_bajo).pack(side="left", padx=2, pady=2)
        
        ttk.Button(top_nav, text="Salir", command=self.mostrar_login).pack(side="right", padx=5, pady=2)
        tk.Label(top_nav, text=f"Almacenista: {nombre_usuario} ({rol})", bg=self.BG_COLOR, fg=self.FG_COLOR, font=("Helvetica", 10, "bold")).pack(side="right", padx=15)

        scan_frame = tk.Frame(frame, bg="white", pady=15, padx=20, relief="ridge", bd=2)
        scan_frame.pack(fill="x", padx=10, pady=10)

        tk.Label(scan_frame, text="REGISTRO RÁPIDO DE ALMACÉN", font=("Helvetica", 12, "bold"), bg="white", fg=self.FG_COLOR).pack(side="top", anchor="w", pady=(0,10))

        control_frame = tk.Frame(scan_frame, bg="white")
        control_frame.pack(fill="x")

        tk.Label(control_frame, text="Código:", font=("Helvetica", 11, "bold"), bg="white", fg=self.FG_COLOR).pack(side="left", padx=(5, 5))
        self.entry_codigo = ttk.Entry(control_frame, font=("Helvetica", 12), width=18)
        self.entry_codigo.pack(side="left", padx=5)
        self.entry_codigo.bind('<Return>', lambda e: self.procesar_movimiento(tipo_mov="ENTRADA"))

        tk.Label(control_frame, text="Cantidad:", font=("Helvetica", 11, "bold"), bg="white", fg=self.FG_COLOR).pack(side="left", padx=(15, 5))
        self.entry_cant = ttk.Entry(control_frame, font=("Helvetica", 12), width=8)
        self.entry_cant.insert(0, "1")
        self.entry_cant.pack(side="left", padx=5)
        self.entry_cant.bind('<Return>', lambda e: self.procesar_movimiento(tipo_mov="ENTRADA"))

        btn_entrada = tk.Button(control_frame, text="🟢 ENTRADA", font=("Helvetica", 11, "bold"), bg="#27ae60", fg="white", relief="flat", cursor="hand2", command=lambda: self.procesar_movimiento(tipo_mov="ENTRADA"))
        btn_entrada.pack(side="left", padx=(20, 5), ipadx=10, ipady=3)
        
        btn_salida = tk.Button(control_frame, text="🔴 SALIDA", font=("Helvetica", 11, "bold"), bg="#c0392b", fg="white", relief="flat", cursor="hand2", command=lambda: self.procesar_movimiento(tipo_mov="SALIDA"))
        btn_salida.pack(side="left", padx=5, ipadx=10, ipady=3)

        ttk.Button(control_frame, text="🔍 Buscar Producto", command=self.ventana_buscar_producto).pack(side="right")

        table_frame = tk.Frame(frame, padx=10, pady=5, bg=self.BG_COLOR)
        table_frame.pack(fill="both", expand=True)

        tk.Label(table_frame, text="BITÁCORA DE MOVIMIENTOS RECIENTES", font=("Helvetica", 11, "bold"), bg=self.BG_COLOR, fg=self.FG_COLOR).pack(anchor="w")

        columnas = ("hora", "codigo", "descripcion", "operacion", "cantidad", "stock")
        self.tree = ttk.Treeview(table_frame, columns=columnas, show="headings", selectmode="extended")
        
        self.tree.heading("hora", text="Hora")
        self.tree.heading("codigo", text="Código")
        self.tree.heading("descripcion", text="Descripción del Producto")
        self.tree.heading("operacion", text="Operación")
        self.tree.heading("cantidad", text="Cant. Movida")
        self.tree.heading("stock", text="Stock Final")

        self.tree.column("hora", width=100, anchor="center")
        self.tree.column("codigo", width=120, anchor="center")
        self.tree.column("descripcion", width=350, anchor="w")
        self.tree.column("operacion", width=120, anchor="center")
        self.tree.column("cantidad", width=100, anchor="center")
        self.tree.column("stock", width=100, anchor="center")

        self.tree.tag_configure("ENTRADA", foreground="#1e8449", background="#e8f8f5")
        self.tree.tag_configure("SALIDA", foreground="#922b21", background="#fdedec")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        bottom_frame = tk.Frame(frame, bg="white", bd=1, relief="solid", padx=20, pady=10)
        bottom_frame.pack(fill="x", side="bottom")

        self.lbl_estado = tk.Label(bottom_frame, text="Sistema listo. Ingresa un código y selecciona Entrada o Salida.", font=("Helvetica", 11), bg="white", fg="#555")
        self.lbl_estado.pack(side="left")

        self.cambiar_frame(frame)
        self.entry_codigo.focus()

    def procesar_movimiento(self, event=None, tipo_mov="ENTRADA"):
        codigo = self.entry_codigo.get().strip()
        cant_str = self.entry_cant.get().strip()

        if not codigo:
            return

        try:
            cant = int(cant_str)
            if cant <= 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Error", "La cantidad debe ser un número entero mayor a 0.")
            self.entry_cant.delete(0, tk.END)
            self.entry_cant.insert(0, "1")
            return

        producto = self.db.obtener_uno(codigo)
        
        if not producto:
            messagebox.showwarning("No encontrado", f"El producto con código '{codigo}' no existe.")
            self.entry_codigo.delete(0, tk.END)
            return

        if tipo_mov == "ENTRADA":
            producto['cantidad'] += cant
        elif tipo_mov == "SALIDA":
            if cant > producto['cantidad']:
                messagebox.showerror("Stock Insuficiente", f"No puedes sacar {cant} unidades.\nSolo hay {producto['cantidad']} en existencia de '{producto['nombre']}'.")
                return
            producto['cantidad'] -= cant

        self.db.actualizar(producto)
        self.db.guardar_movimiento(codigo, tipo_mov, cant)

        hora_actual = datetime.now().strftime("%H:%M:%S")
        self.tree.insert("", 0, values=(
            hora_actual,
            producto['id'], 
            producto['nombre'], 
            f"🟢 ENTRADA" if tipo_mov == "ENTRADA" else f"🔴 SALIDA",
            f"+{cant}" if tipo_mov == "ENTRADA" else f"-{cant}",
            producto['cantidad']
        ), tags=(tipo_mov,))

        self.lbl_estado.config(text=f"Último movimiento: {tipo_mov} de {cant}x {producto['nombre']} | Nuevo stock: {producto['cantidad']}")

        if producto['cantidad'] <= producto['stock_minimo']:
            messagebox.showwarning("Alerta de Stock", f"¡ATENCIÓN! El producto '{producto['nombre']}' ha llegado a su nivel de stock mínimo ({producto['cantidad']} restantes).")
            self.inv.cola.encolar(codigo)

        self.entry_codigo.delete(0, tk.END)
        self.entry_cant.delete(0, tk.END)
        self.entry_cant.insert(0, "1")
        self.entry_codigo.focus()

if __name__ == "__main__":
    app = AplicacionAbarrotes()
    app.mainloop()
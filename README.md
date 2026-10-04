# Sistema de Control de Inventarios
**Equipo 1 | Empresa: Abarrotes Los Lobos**  
Materia: Estructura de Datos

---

## Descripción
Sistema de consola desarrollado en **Python** para gestionar el inventario de una tienda de abarrotes. Permite registrar productos, controlar entradas y salidas de mercancía, detectar stock bajo y generar reportes. Implementa estructuras de datos (Pila, Cola, Recursividad), base de datos SQLite y control de acceso por roles.

---

## Requisitos
- **Python 3.10 o superior** (se usa `match/case` que requiere esta versión)
- No requiere instalar librerías adicionales. Todo lo que se usa (`sqlite3`, `csv`, `os`) viene incluido con Python.

---

## Estructura del Proyecto

```
ProyectoEstructura/
│
├── main.py                → Login, menús por rol y punto de entrada.
├── inventario.py          → Clase Inventario con todas las operaciones.
├── database.py            → Clase Database. Maneja SQLite3.
├── estructura_datos.py    → Clases Pila, Cola y función recursiva.
│
├── inventario.db          → Base de datos (se crea automáticamente al correr)
│
├── EXPLICACION_CODIGO.txt → Explicación detallada del código
└── README.md              → Este archivo
```



---

## Usuarios y Roles

El sistema tiene **control de acceso por rol**. Cada usuario solo ve las opciones que le corresponden.

| Usuario | Contraseña | Rol |
|---------|-----------|-----|
| `gerente` | `123` | Gerente |
| `almacen` | `123` | Almacen |
| `admin` | `123` | Administrador |

> Los usuarios se guardan en la base de datos. Al correr el programa por primera vez se crean los tres usuarios de arriba automáticamente. El Gerente puede agregar más usuarios desde el menú.

> El sistema permite **3 intentos** de inicio de sesión. Si los 3 fallan, el programa se cierra. Al cerrar sesión desde el menú, el programa regresa al login en lugar de terminar.

---

## Menú por Rol

### Gerente — Acceso completo

| Opción | Función |
|--------|---------|
| 1 | Registrar producto |
| 2 | Consultar todos los productos |
| 3 | Buscar producto |
| 4 | Modificar producto |
| 5 | Eliminar producto |
| 6 | Entrada de mercancía |
| 7 | Salida de mercancía |
| 8 | Detectar stock bajo |
| 9 | Reporte general |
| 10 | Exportar a CSV |
| 11 | Importar desde CSV |
| 12 | Cola de resurtido |
| 13 | Gestión de usuarios |
| 0 | Cerrar sesión |

### Encargado de Almacén — Solo movimientos de mercancía

| Opción | Función |
|--------|---------|
| 1 | Entrada de mercancía |
| 2 | Salida de mercancía |
| 3 | Consultar stock bajo |
| 4 | Cola de resurtido |
| 0 | Cerrar sesión |

### Administrador — Solo consulta y reportes

| Opción | Función |
|--------|---------|
| 1 | Consultar todos los productos |
| 2 | Buscar producto |
| 3 | Detectar stock bajo |
| 4 | Reporte general |
| 5 | Exportar a CSV |
| 0 | Cerrar sesión |

---

## Gestión de Usuarios (solo Gerente)

Desde la opción **13** del menú de Gerente:
- **Ver usuarios**: muestra todos los usuarios y sus roles.
- **Dar de alta**: crea un nuevo usuario eligiendo nombre, contraseña y rol.
- **Eliminar**: borra un usuario (los usuarios del sistema `gerente`, `almacen` y `admin` no se pueden borrar).

---

## Datos del Producto

| Campo | Tipo | Descripción |
|-------|------|-------------|
| ID | Texto | Código único del producto (ej. P001) |
| Nombre | Texto | Nombre del artículo |
| Descripción | Texto | Descripción adicional (opcional) |
| Categoría | Texto | Tipo (ej. Abarrotes, Limpieza) |
| Precio | Decimal | Precio de venta en pesos |
| Cantidad | Entero | Unidades disponibles en almacén |
| Stock mínimo | Entero | Cantidad mínima antes de alertar |

---

## Exportar / Importar CSV

### Exportar
- Selecciona la opción de exportar en el menú.
- Se genera `inventario_exportado.csv` en la misma carpeta.
- Puede abrirse en **Microsoft Excel**.

### Importar
- Prepara un CSV con las columnas: `id,nombre,descripcion,categoria,precio,cantidad,stock_minimo`
- La primera fila debe ser el encabezado.
- Los productos con ID repetido se omiten automáticamente.
- Las filas con datos mal formateados (campos vacíos, texto en campos numéricos, columnas faltantes) se omiten con aviso del número de fila, sin detener el programa.

**Ejemplo:**
```
id,nombre,descripcion,categoria,precio,cantidad,stock_minimo
P001,Arroz,Arroz blanco 1kg,Abarrotes,25.00,100,20
P002,Frijol,Frijol negro 1kg,Abarrotes,30.00,80,15
```

---

## Estructuras de Datos

| Estructura | Dónde se usa |
|---|---|
| **Lista** | Resultados de consultas a SQLite (temporales) |
| **Diccionario** | Cada producto y cada usuario es un diccionario |
| **Pila (LIFO)** | Historial de movimientos de la sesión actual |
| **Cola (FIFO)** | Productos con stock bajo esperando resurtido en orden |
| **Recursividad** | `buscar_en_lista()` en `estructura_datos.py` |

---

## Base de Datos — Tablas SQLite

| Tabla | Contenido |
|---|---|
| `productos` | Todos los productos registrados |
| `movimientos` | Historial de entradas y salidas con fecha |
| `usuarios` | Usuarios del sistema con su rol y contraseña |

Todos los accesos a la base de datos están protegidos con `try-except sqlite3.Error`. Los métodos de escritura (INSERT, UPDATE, DELETE) incluyen `con.rollback()` ante cualquier falla para garantizar que la base de datos no quede en un estado corrupto. El bloque `finally` asegura que la conexión siempre se cierre.

---

## Checklist de Pruebas

- [x] Login rechaza credenciales incorrectas (3 intentos máximo)
- [x] El menú que aparece es diferente según el rol
- [x] El Encargado de Almacén NO puede registrar ni eliminar productos
- [x] El Administrador solo puede consultar, no modificar
- [x] No se registran dos productos con el mismo ID
- [x] Precio y cantidad rechazan texto (solo números)
- [x] No se puede sacar más mercancía de la que hay
- [x] Al quedar stock bajo, aparece aviso y entra a la cola
- [x] Eliminar producto pide confirmación antes de borrar
- [x] Reporte muestra los últimos movimientos correctamente
- [x] El Gerente puede crear y eliminar usuarios desde opción 13
- [x] Los usuarios `gerente`, `almacen` y `admin` no se pueden borrar
- [x] Exportar genera `inventario_exportado.csv` correctamente
- [x] Importar omite productos con ID duplicado sin romper el programa
- [x] Importar omite filas con datos inválidos mostrando aviso por fila
- [x] Al cerrar y volver a abrir, los datos siguen guardados (SQLite)
- [x] Búsqueda recursiva encuentra coincidencia exacta por nombre
- [x] Cerrar sesión regresa al Login sin terminar el programa
- [x] Errores de SQLite no causan crash del programa
- [x] Fallos en escritura de BD hacen rollback para mantener integridad

---

*Equipo 1 – Control de Inventarios*

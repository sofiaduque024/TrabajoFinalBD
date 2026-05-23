import psycopg2

CADENA_CONEXION = "postgresql://postgres.vxmhufptarfyswpnvvra:[CONTRASEÑA]@aws-1-us-west-2.pooler.supabase.com:5432/postgres"

def conectar():
    conexion = psycopg2.connect(
        host="aws-1-us-west-2.pooler.supabase.com",
        port="5432",
        database="postgres",
        user="postgres.vxmhufptarfyswpnvvra",
        password="CONTRASEÑA"  
    )
    return conexion


#TABLA: clientes
def crear_cliente(nombre_cliente, telefono_cliente, ciudad_cliente):
    try:
        conexion = conectar()
        cursor   = conexion.cursor()
        consulta_sql = """
            INSERT INTO public.clientes (nombre_cliente, telefono_cliente, ciudad_cliente)
            VALUES (%s, %s, %s)
        """
        cursor.execute(consulta_sql, (nombre_cliente, telefono_cliente, ciudad_cliente))
        conexion.commit()
        print(f"Cliente '{nombre_cliente}' creado correctamente.")

    except psycopg2.errors.UniqueViolation:
        print(f"El teléfono '{telefono_cliente}' ya está registrado. Usa uno diferente.")
        conexion.rollback()
    except psycopg2.Error as error_bd:
        print(f"Error al crear cliente: {error_bd}")
        conexion.rollback()


def leer_clientes():
    try:
        conexion = conectar()
        cursor   = conexion.cursor()
        cursor.execute("SELECT id_cliente, nombre_cliente, telefono_cliente, ciudad_cliente FROM public.clientes")
        lista_clientes = cursor.fetchall()
        print("\n📋 LISTA DE CLIENTES:")
        print("-" * 60)
        if len(lista_clientes) == 0:
            print("No hay clientes registrados.")
        else:
            for cliente in lista_clientes:
                id_cliente     = cliente[0]
                nombre_cliente = cliente[1]
                telefono       = cliente[2]
                ciudad         = cliente[3]
                print(f"ID: {id_cliente} | Nombre: {nombre_cliente} | Tel: {telefono} | Ciudad: {ciudad}")
        print("-" * 60)
    except psycopg2.Error as error_bd:
        print(f"Error al consultar clientes: {error_bd}")
        conexion.rollback()


def buscar_cliente_por_id(id_cliente):
    try:
        conexion = conectar()
        cursor   = conexion.cursor()
        consulta_sql = """
            SELECT id_cliente, nombre_cliente, telefono_cliente, ciudad_cliente
            FROM public.clientes
            WHERE id_cliente = %s
        """
        cursor.execute(consulta_sql, (id_cliente,))
        cliente_encontrado = cursor.fetchone()
        if cliente_encontrado is None:
            print(f"No se encontró ningún cliente con ID {id_cliente}.")
        else:
            print(f"Cliente encontrado:")
            print(f"ID:{cliente_encontrado[0]}")
            print(f"Nombre:{cliente_encontrado[1]}")
            print(f"Teléfono:{cliente_encontrado[2]}")
            print(f"Ciudad:{cliente_encontrado[3]}")
    except psycopg2.Error as error_bd:
        print(f"Error al buscar cliente: {error_bd}")
        conexion.rollback()


def actualizar_cliente(id_cliente, nuevo_nombre, nuevo_telefono, nueva_ciudad):
    try:
        conexion = conectar()
        cursor   = conexion.cursor()
        consulta_sql = """
            UPDATE public.clientes
            SET nombre_cliente   = %s,
                telefono_cliente = %s,
                ciudad_cliente   = %s
            WHERE id_cliente = %s
        """
        cursor.execute(consulta_sql, (nuevo_nombre, nuevo_telefono, nueva_ciudad, id_cliente))
        conexion.commit()
        if cursor.rowcount == 0:
            print(f"No se encontró ningún cliente con ID {id_cliente}.")
        else:
            print(f"Cliente con ID {id_cliente} actualizado correctamente.")
    except psycopg2.errors.UniqueViolation:
        print(f"El teléfono '{nuevo_telefono}' ya está registrado. Usa uno diferente.")
        conexion.rollback()
    except psycopg2.Error as error_bd:
        print(f"Error al actualizar cliente: {error_bd}")
        conexion.rollback()


def eliminar_cliente(id_cliente):
    try:
        conexion = conectar()
        cursor   = conexion.cursor()
        cursor.execute("DELETE FROM public.clientes WHERE id_cliente = %s", (id_cliente,))
        conexion.commit()
        if cursor.rowcount == 0:
            print(f"No se encontró ningún cliente con ID {id_cliente}.")
        else:
            print(f"Cliente con ID {id_cliente} eliminado correctamente.")
    except psycopg2.errors.ForeignKeyViolation:
        print(f"No se puede eliminar: el cliente {id_cliente} tiene órdenes asociadas.")
        conexion.rollback()
    except psycopg2.Error as error_bd:
        print(f"Error al eliminar cliente: {error_bd}")
        conexion.rollback()


#  CRUD - TABLA: productos
def crear_producto(nombre_producto, precio_producto, stock, id_categoria):
    """Inserta un nuevo producto en la base de datos."""
    try:
        conexion = conectar()
        cursor   = conexion.cursor()
        consulta_sql = """
            INSERT INTO public.productos (nombre_producto, precio_producto, stock, id_categoria)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(consulta_sql, (nombre_producto, precio_producto, stock, id_categoria))
        conexion.commit()
        print(f"Producto '{nombre_producto}' creado correctamente.")
    except psycopg2.errors.ForeignKeyViolation:
        print(f"La categoría con ID {id_categoria} no existe. Verifica el ID.")
        conexion.rollback()
    except psycopg2.errors.CheckViolation:
        print(f"El precio debe ser mayor a 0 y el stock no puede ser negativo.")
        conexion.rollback()
    except psycopg2.Error as error_bd:
        print(f"Error al crear producto: {error_bd}")
        conexion.rollback()


def leer_productos():
    try:
        conexion = conectar()
        cursor   = conexion.cursor()
        cursor.execute("SELECT id_producto, nombre_producto, precio_producto, stock, id_categoria FROM public.productos")
        lista_productos = cursor.fetchall()
        print("LISTA DE PRODUCTOS:")
        if len(lista_productos) == 0:
            print("No hay productos registrados.")
        else:
            for producto in lista_productos:
                id_producto     = producto[0]
                nombre_producto = producto[1]
                precio          = producto[2]
                stock           = producto[3]
                id_categoria    = producto[4]
                print(f"ID: {id_producto} | {nombre_producto} | Precio: ${precio:,} | Stock: {stock} | Categoría ID: {id_categoria}")
    except psycopg2.Error as error_bd:
        print(f"Error al consultar productos: {error_bd}")
        conexion.rollback()


def buscar_producto_por_id(id_producto):
    try:
        conexion = conectar()
        cursor   = conexion.cursor()
        consulta_sql = """
            SELECT id_producto, nombre_producto, precio_producto, stock, id_categoria
            FROM public.productos
            WHERE id_producto = %s
        """
        cursor.execute(consulta_sql, (id_producto,))
        producto_encontrado = cursor.fetchone()
        if producto_encontrado is None:
            print(f"No se encontró ningún producto con ID {id_producto}.")
        else:
            print(f"Producto encontrado:")
            print(f"ID:{producto_encontrado[0]}")
            print(f"Nombre:{producto_encontrado[1]}")
            print(f"Precio:${producto_encontrado[2]:,}")
            print(f"Stock:{producto_encontrado[3]}")
            print(f"Categoría ID:{producto_encontrado[4]}")
    except psycopg2.Error as error_bd:
        print(f"Error al buscar producto: {error_bd}")
        conexion.rollback()


def actualizar_producto(id_producto, nuevo_nombre, nuevo_precio, nuevo_stock, nueva_categoria):
    try:
        conexion = conectar()
        cursor   = conexion.cursor()
        consulta_sql = """
            UPDATE public.productos
            SET nombre_producto = %s,
                precio_producto = %s,
                stock           = %s,
                id_categoria    = %s
            WHERE id_producto = %s
        """
        cursor.execute(consulta_sql, (nuevo_nombre, nuevo_precio, nuevo_stock, nueva_categoria, id_producto))
        conexion.commit()
        if cursor.rowcount == 0:
            print(f"No se encontró ningún producto con ID {id_producto}.")
        else:
            print(f"Producto con ID {id_producto} actualizado correctamente.")
    except psycopg2.errors.CheckViolation:
        print(f"El precio debe ser mayor a 0 y el stock no puede ser negativo.")
        conexion.rollback()
    except psycopg2.errors.ForeignKeyViolation:
        print(f"La categoría con ID {nueva_categoria} no existe. Verifica el ID.")
        conexion.rollback()
    except psycopg2.Error as error_bd:
        print(f"Error al actualizar producto: {error_bd}")
        conexion.rollback()


def eliminar_producto(id_producto):
    try:
        conexion = conectar()
        cursor   = conexion.cursor()
        cursor.execute("DELETE FROM public.productos WHERE id_producto = %s", (id_producto,))
        conexion.commit()
        if cursor.rowcount == 0:
            print(f"No se encontró ningún producto con ID {id_producto}.")
        else:
            print(f"Producto con ID {id_producto} eliminado correctamente.")
    except psycopg2.errors.ForeignKeyViolation:
        print(f"No se puede eliminar: el producto {id_producto} está en órdenes registradas.")
        conexion.rollback()
    except psycopg2.Error as error_bd:
        print(f"Error al eliminar producto: {error_bd}")
        conexion.rollback()


#  MENÚ PRINCIPAL
def mostrar_menu():
    print("SISTEMA CRUD - BIKE ZONE")
    print("CLIENTES")
    print("1. Ver todos los clientes")
    print("2. Buscar cliente por ID")
    print("3. Crear nuevo cliente")
    print("4. Actualizar cliente")
    print("5. Eliminar cliente")
    print("PRODUCTOS")
    print("6. Ver todos los productos")
    print("7. Buscar producto por ID")
    print("8. Crear nuevo producto")
    print("9. Actualizar producto")
    print("10. Eliminar producto")
    print("0. Salir")
    opcion_elegida = input("Elige una opción: ")
    return opcion_elegida


def main():
    continuar = True
    while continuar:
        opcion = mostrar_menu()

        if opcion == "1":
            leer_clientes()
        elif opcion == "2":
            try:
                id_buscado = int(input("Ingresa el ID del cliente: "))
                buscar_cliente_por_id(id_buscado)
            except ValueError:
                print("El ID debe ser un número entero.")
        elif opcion == "3":
            nombre   = input("Nombre del cliente: ")
            telefono = input("Teléfono (10 dígitos): ")
            ciudad   = input("Ciudad: ")
            crear_cliente(nombre, telefono, ciudad)
        elif opcion == "4":
            try:
                id_actualizar  = int(input("ID del cliente a actualizar: "))
                nuevo_nombre   = input("Nuevo nombre: ")
                nuevo_telefono = input("Nuevo teléfono (10 dígitos): ")
                nueva_ciudad   = input("Nueva ciudad: ")
                actualizar_cliente(id_actualizar, nuevo_nombre, nuevo_telefono, nueva_ciudad)
            except ValueError:
                print("El ID debe ser un número entero.")
        elif opcion == "5":
            try:
                id_eliminar = int(input("ID del cliente a eliminar: "))
                confirmar   = input(f"¿Seguro que quieres eliminar el cliente {id_eliminar}? (s/n): ")
                if confirmar.lower() == "s":
                    eliminar_cliente(id_eliminar)
                else:
                    print("Operación cancelada.")
            except ValueError:
                print("El ID debe ser un número entero.")
        elif opcion == "6":
            leer_productos()
        elif opcion == "7":
            try:
                id_buscado = int(input("Ingresa el ID del producto: "))
                buscar_producto_por_id(id_buscado)
            except ValueError:
                print("El ID debe ser un número entero.")
        elif opcion == "8":
            try:
                nombre    = input("Nombre del producto: ")
                precio    = float(input("Precio: "))
                stock     = int(input("Stock inicial: "))
                categoria = int(input("ID de categoría (1=Mountain, 2=Road, 3=Electric, 4=Accesorios, 5=Kids, 6=BMX): "))
                crear_producto(nombre, precio, stock, categoria)
            except ValueError:
                print("El precio debe ser un número. El stock y categoría deben ser enteros.")
        elif opcion == "9":
            try:
                id_actualizar   = int(input("ID del producto a actualizar: "))
                nuevo_nombre    = input("Nuevo nombre: ")
                nuevo_precio    = float(input("Nuevo precio: "))
                nuevo_stock     = int(input("Nuevo stock: "))
                nueva_categoria = int(input("Nueva categoría ID: "))
                actualizar_producto(id_actualizar, nuevo_nombre, nuevo_precio, nuevo_stock, nueva_categoria)
            except ValueError:
                print("El precio debe ser un número. El stock y categoría deben ser enteros.")
        elif opcion == "10":
            try:
                id_eliminar = int(input("ID del producto a eliminar: "))
                confirmar   = input(f"¿Seguro que quieres eliminar el producto {id_eliminar}? (s/n): ")
                if confirmar.lower() == "s":
                    eliminar_producto(id_eliminar)
                else:
                    print("Operación cancelada.")
            except ValueError:
                print("El ID debe ser un número entero.")
        elif opcion == "0":
            print("\n¡Hasta luego!")
            continuar = False
        else:
            print("Opción no válida. Intenta de nuevo.")


# Punto de entrada del programa
if __name__ == "__main__":
    main()

#from redis_db import redis_db
from users import get_session,get_categoria_by_user_id
from redis_db import connect_redis 
from cassandra_db import connect_cassandra
from catalogo import get_product_price

import uuid
from datetime import datetime

# Conexión a Redis
redis_client = connect_redis()

# Agregar un producto al carrito
def add_to_cart(user_id, product_id, quantity):
    if not get_session(user_id):
        print("El usuario no tiene una sesión activa.")
        return
    
    cart_key = f"cart:{user_id}"
    int(quantity)
    redis_client.hincrby(cart_key, product_id, quantity)
    print(f"🛒 Producto {product_id} agregado al carrito del usuario {user_id}")

# Obtener productos en el carrito
def get_cart(user_id):
    if not get_session(user_id):
        print("El usuario no tiene una sesión activa.")
        return
    cart_key = f"cart:{user_id}"
    cart = redis_client.hgetall(cart_key)
    return cart

# Vaciar el carrito después de realizar una compra
def clear_cart(user_id):
    if not get_session(user_id):
        print("El usuario no tiene una sesión activa.")
        return
    cart_key = f"cart:{user_id}"
    redis_client.delete(cart_key)
    print(f"🗑️ Carrito del usuario {user_id} vaciado")


 # necesitamos id_user  , id carrito, categoria usuario ,  crea dato en cassandra con informacion de usuario [ importe , descuento, monto]

# Función para convertir carrito a pedido, incluyendo impuestos, descuentos forma de pago
def convertir_carrito(user_id, forma_pago):
    if not get_session(user_id):
        print("El usuario no tiene una sesión activa.")
        return

    # Obtener el carrito desde Redis
    cart = get_cart(user_id)
    if not cart:
        print("El carrito está vacío.")
        return

    # Conexión a Cassandra
    session = connect_cassandra()

    # Asegurarse de usar el keyspace adecuado
    session.execute("USE tu_keyspace")


    # Crear tabla de pedidos si no existe
    session.execute("""
        CREATE TABLE IF NOT EXISTS pedidos (
            order_id UUID PRIMARY KEY,
            user_id TEXT,
            productos MAP<TEXT, INT>,
            fecha TIMESTAMP,
            total DECIMAL,
            impuestos DECIMAL,
            descuento DECIMAL,
            forma_pago TEXT
        )
    """)


    session.execute("""
    CREATE INDEX IF NOT EXISTS user_id_index ON pedidos (user_id);
    """)


    # Generar un ID único para el pedido
    order_id = uuid.uuid4()

    # Convertir las claves a str y los valores a int
    cart = {str(k): int(v) for k, v in cart.items()}

    # Calcular el total, descuentos e impuestos
    total = 0
    descuento = 0
    impuestos = 0

    # Aquí puedes agregar la lógica para obtener el precio de cada producto y calcular descuentos por categoría
    for product_id, quantity in cart.items():
        # Lógica para obtener el precio del producto
        # Esto debe ser implementado según cómo se gestionan los productos en tu sistema
        precio_producto = obtener_precio_producto(user_id,product_id)
        print(precio_producto)  #int


        # Si el producto tiene algún descuento por categoría, lo aplicamos aquí
        categoria = get_categoria_by_user_id(user_id)

        if categoria == "low":
            descuento_producto = 0
        elif categoria == "med":
            descuento_producto = 5
        else:
            descuento_producto = 10  # Descuento del 10% para categoría "high"
          #si low es 0 , si es med 5 , high 10 
        descuento += precio_producto * descuento_producto *int(quantity)*0.01
     
        # Calcular el precio total antes de impuestos
        total += precio_producto * int(quantity)

    # Aplicar IVA del 21%
    impuestos = total * 0.21
    total_con_impuestos = total + impuestos - descuento

    # Insertar el pedido con los detalles del pago en Cassandra
    session.execute("""
        INSERT INTO pedidos (order_id, user_id, productos, fecha, total, impuestos, descuento, forma_pago)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (order_id, user_id, cart, datetime.utcnow(), total_con_impuestos, impuestos, descuento, forma_pago))

    print(f"📦 Pedido {order_id} creado para el usuario {user_id}")
    print(f"Total: {total_con_impuestos} | IVA: {impuestos} | Descuento: {descuento} | Forma de pago: {forma_pago}")

    # Vaciar el carrito en Redis después de crear el pedido
    clear_cart(user_id)

# Función para obtener el precio de un producto (simulada)
def obtener_precio_producto(user_id,product_id):
    # Aquí deberías buscar el precio real del producto en la base de datos o sistema

    get_product_price(user_id,product_id)
    precios_simulados = {
        '1': 100,  # Precio del producto con ID 1
        '2': 200,  # Precio del producto con ID 2
    }


    return precios_simulados.get(product_id, 0)

# Función para obtener el descuento por categoría (simulada)
def obtener_descuento_por_categoria(product_id):
    # Aquí deberías buscar el descuento por categoría del producto
    descuentos_simulados = {
        '1': 0.10,  # Descuento del 10% para el producto con ID 1
        '2': 0.05,  # Descuento del 5% para el producto con ID 2
    }
    return descuentos_simulados.get(product_id, 0)



def ver_pedidos(user_id):
    """Ver los pedidos de un usuario específico."""
    # Conectar a Cassandra
    session = connect_cassandra()
    print(f"session existe? {session}")

    # Asegurarse de usar el keyspace adecuado
    session.execute("USE tu_keyspace")

    # Consultar los pedidos del usuario
    rows = session.execute("""
        SELECT * FROM pedidos WHERE user_id = %s
    """, (user_id,))

    # Verificar si se encontraron pedidos
    if not rows:
        print(f"No se encontraron pedidos para el usuario {user_id}.")
        return

    # Mostrar los pedidos
    print(f"Pedidos para el usuario {user_id}:")
    for row in rows:
        print(f"Pedido ID: {row.order_id}")
        print(f"Fecha: {row.fecha}")
        print(f"Total: {row.total}")
        print(f"Productos: {row.productos}")
        print(f"IVA: {row.impuestos}")
        print(f"Descuento: {row.descuento}")
        print(f"Forma de pago: {row.forma_pago}")
        print("-" * 50)  # Separador visual

'''
def convertir_carrito(user_id):
    if not get_session(user_id):
        print("El usuario no tiene una sesión activa.")
        return

    # Obtener el carrito desde Redis
    cart = get_cart(user_id)
    if not cart:
        print("El carrito está vacío.")
        return

    # Conexión a Cassandra
    session = connect_cassandra()

    session.execute("""
    CREATE KEYSPACE IF NOT EXISTS tu_keyspace
    WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1'};
    """)
    # Crear tabla de pedidos si no existe
    session.execute("""
        CREATE TABLE IF NOT EXISTS pedidos (
            order_id UUID PRIMARY KEY,
            user_id TEXT,
            productos MAP<TEXT, TEXT>,
            fecha TIMESTAMP
        )
    """)

    # Generar un ID único para el pedido
    order_id = uuid.uuid4()

    # Convertir las claves a str y los valores a int
    cart = {str(k): int(v) for k, v in cart.items()}

    # Insertar el pedido en Cassandra
    session.execute("""
        INSERT INTO pedidos (order_id, user_id, productos, fecha)
        VALUES (%s, %s, %s, %s)
    """, (order_id, user_id, cart, datetime.utcnow()))

    print(f"📦 Pedido {order_id} creado para el usuario {user_id}")

    # Vaciar el carrito en Redis
    clear_cart(user_id)

'''


#----cassandra------


#   Guardar, recuperar y volver a estados anteriores en las acciones realizadas sobre un carrito de compras activo. #sacamos los pedidos de facturas 



#Facturar el pedido y registrar el pago indicando la forma de pago
#funcion CONVERTIR_PEDIDO --> Convertir el contenido del carrito de compras en un pedido con detalles del cliente, 
#importes, descuentos (segun categoria )e impuestos(iva 21%).





#historial de operaciones --> Llevar el control de operaciones de facturación y pagos realizados por los usuarios.

#facturas 
#id, monto(final) ,pedido,fecha


#se actualiza tabla historial  cassandra
#funcion historial de cambios --> Llevar un registro de todas las actividades realizadas sobre el catálogo de productos.
# id producto , comentario(sobre cambio de precio, nombre,etc)  



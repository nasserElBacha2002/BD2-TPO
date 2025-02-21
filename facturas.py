from cassandra_db import connect_cassandra
from datetime import datetime
from users import get_session
import uuid


# Conectar a Cassandra
db_session = connect_cassandra()


# Crear tabla de pedidos si no existe
db_session.execute("""
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

# Crear índice para user_id
db_session.execute("""
    CREATE INDEX IF NOT EXISTS user_id_index ON pedidos (user_id);
""")

# Crear tabla de facturas si no existe
db_session.execute("""
    CREATE TABLE IF NOT EXISTS facturas (
        id UUID PRIMARY KEY,
        monto DECIMAL,
        pedido UUID,
        fecha TIMESTAMP,
        forma_pago TEXT
    )
""")

# Crear tabla de historial_pagos si no existe
db_session.execute("""
    CREATE TABLE IF NOT EXISTS historial_pagos (
        user_id TEXT,
        pedido_id UUID,
        monto DECIMAL,
        fecha TIMESTAMP,
        forma_pago TEXT,
        PRIMARY KEY (user_id, fecha)
    ) WITH CLUSTERING ORDER BY (fecha DESC);
""")

def confirmar_pedido(user_id, pedido_id, monto_final, forma_pago):
    timestamp = datetime.now()
    pedido_id = uuid.UUID(pedido_id)
    # Guardar factura
    db_session.execute("""
        INSERT INTO facturas (id, monto, pedido, fecha, forma_pago)
        VALUES (uuid(), %s, %s, %s, %s)
    """, (monto_final, pedido_id, timestamp, forma_pago))
    
    db_session.execute("""
        INSERT INTO historial_pagos (user_id, pedido_id, monto, fecha, forma_pago)
        VALUES (%s, %s, %s, %s, %s)
    """, (user_id, pedido_id, monto_final, timestamp, forma_pago))
    
    print(f"✅ Pedido {pedido_id} confirmado y facturado para el usuario {user_id}.")

def obtener_pedidos():
    rows = db_session.execute("""
        SELECT pedido_id, monto, fecha FROM historial_pagos """)
    
    pedidos = [row._asdict() for row in rows]
    return pedidos

def obtener_ultimo_pedido(user_id):
    if not get_session(user_id):  # Verificación de sesión activa
        print("El usuario no tiene una sesión activa.")
        return None  # Retornar None si no hay sesión activa
    
    row = db_session.execute("""
        SELECT pedido_id, monto, fecha FROM historial_pagos 
        WHERE user_id = %s ORDER BY fecha DESC LIMIT 1
    """, (user_id,)).one()

    if row:
        return row._asdict()  # Usar _asdict() si la fila es un namedtuple
    else:
        print("No se encontró el último pedido para este usuario.")
        return None  # Retornar None si no se encuentra el pedido

def obtener_facturas():
    print(db_session)
    rows= db_session.execute(""" SELECT pedido_id FROM historial_pagos""")
    
    facturas = [row._asdict() for row in rows]
    return facturas

from cassandra_db import connect_cassandra
from datetime import datetime
from users import get_session

# Conectar a Cassandra
db_session = connect_cassandra()

def confirmar_pedido(user_id, pedido_id, monto_final, forma_pago):
    timestamp = datetime.now()
    
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
    
    pedidos = [dict(row) for row in rows]
    return pedidos

def obtener_ultimo_pedido(user_id):
    if not get_session(user_id):
        print("El usuario no tiene una sesión activa.")
        return
    row = db_session.execute("""
        SELECT pedido_id, monto, fecha FROM historial_pagos WHERE user_id = %s ORDER BY fecha DESC LIMIT 1
    """, (user_id,)).one()
    
    return dict(row) if row else None

def obtener_facturas():
    rows = db_session.execute(""" SELECT pedido_id FROM historial_pagos""")
    
    facturas = [dict(row) for row in rows]
    return facturas

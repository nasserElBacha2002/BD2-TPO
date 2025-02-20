#from redis_db import redis_db
from redis_db import connect_redis 
from users import get_session

# Conexión a Redis
client = connect_redis()

def update_price(product_id, price):
    product_key = f"product:{product_id}"
    if client.exists(product_key):
        client.hset(product_key, mapping={
            'price': price
        })
        print(f"Producto con ID {product_id} actualizado.")
    else:
       client.hset(product_key, mapping={
        'price': price
    })

def get_product_price(user_id,product_id):
    if not get_session(user_id):
        print("El usuario no tiene una sesión activa.")
        return
    product_key = f"product:{product_id}"
    price = client.hget(product_key, 'price')
    if price:
        print(f"El precio del producto con ID {product_id} es: {price}")
    else:
        print(f"Producto con ID {product_id} no encontrado.")



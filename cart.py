#from redis_db import redis_db
from redis_db import connect_redis 

# Conexión a Redis
redis_client = connect_redis()

# Agregar un producto al carrito
def add_to_cart(user_id, product_id, quantity):
    cart_key = f"cart:{user_id}"
    redis_client.hincrby(cart_key, product_id, quantity)
    print(f"🛒 Producto {product_id} agregado al carrito del usuario {user_id}")

# Obtener productos en el carrito
def get_cart(user_id):
    cart_key = f"cart:{user_id}"
    cart = redis_client.hgetall(cart_key)
    return cart

# Vaciar el carrito después de realizar una compra
def clear_cart(user_id):
    cart_key = f"cart:{user_id}"
    redis_client.delete(cart_key)
    print(f"🗑️ Carrito del usuario {user_id} vaciado")

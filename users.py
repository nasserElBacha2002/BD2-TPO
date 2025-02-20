from mongo import connect_mongodb
from redis_db import connect_redis

# Conexión única
db = connect_mongodb()
redis_client = connect_redis()

# --- Funciones de Usuarios ---
def create_user(email, password, user_id, cantidad_compras):
    usuarios = db["usuarios"]
    
    if usuarios.find_one({"id": user_id}):
        print(f"El usuario con ID {user_id} ya existe.")
        return

    user_data = {
        "email": email,
        "password": password,
        "id": user_id,
        "cantidad_compras": cantidad_compras
    }
    result = usuarios.insert_one(user_data)
    print(f"Usuario creado con ID: {result.inserted_id}")

def get_user_by_id(user_id):
    usuarios = db["usuarios"]
    return usuarios.find_one({"id": user_id})

# --- Funciones de Categorización ---
def create_categoria(user_id, categoria):
    if not get_session(user_id):
        print("El usuario no tiene una sesión activa.")
        return
    categorizacion = db["categorizacion"]

    if categorizacion.find_one({"id_usuario": user_id}):
        categorizacion.update_one(
            {"id_usuario": user_id}, 
            {"$set": {"categoria": categoria}}
        )
        print(f"Categoría de usuario {user_id} actualizada a {categoria}")
    else:
        result = categorizacion.insert_one({"id_usuario": user_id, "categoria": categoria})
        print(f"Categorización creada para el usuario con ID: {result.inserted_id}")

def get_categoria_by_user_id(user_id):
    categorizacion = db["categorizacion"]
    return categorizacion.find_one({"id_usuario": user_id})

def update_categoria_automatica(user_id):
    if not get_session(user_id):
        print("El usuario no tiene una sesión activa.")
        return
    user = get_user_by_id(user_id)
    if user:
        cantidad_compras = user["cantidad_compras"]
        categoria = "LOW" if cantidad_compras <= 5 else "MEDIUM" if cantidad_compras <= 10 else "TOP"
        create_categoria(user_id, categoria)

# --- Funciones de Productos ---
def create_producto(nombre, descripcion, producto_id):
    
    productos = db["productos"]
    
    if productos.find_one({"id": producto_id}):
        print(f"El producto con ID {producto_id} ya existe.")
        return

    result = productos.insert_one({"id": producto_id, "nombre": nombre, "descripcion": descripcion})
    print(f"Producto creado con ID: {result.inserted_id}")

def get_producto_by_id(user_id,producto_id):
    if user_id and not get_session(user_id):
        print("El usuario no tiene una sesión activa.")
        return
    productos = db["productos"]
    
    return productos.find_one({"id": producto_id})   

def update_producto(producto_id, nombre=None, descripcion=None, user_id=None):
    
    productos = db["productos"]
    
    update_data = {}
    if nombre:
        update_data["nombre"] = nombre
    if descripcion:
        update_data["descripcion"] = descripcion

    if not update_data:
        print("No hay datos para actualizar.")
        return

    result = productos.update_one({"id": producto_id}, {"$set": update_data})
    if result.modified_count > 0:
        print(f"Producto con ID {producto_id} actualizado correctamente")
    else:
        print(f"No se realizaron cambios en el producto con ID {producto_id}")

def delete_producto(producto_id):
    
    productos = db["productos"]
    
    if not productos.find_one({"id": producto_id}):
        print(f"Producto con ID {producto_id} no encontrado.")
        return

    result = productos.delete_one({"id": producto_id})
    if result.deleted_count > 0:
        print(f"Producto con ID {producto_id} eliminado correctamente")

def delete_categoria(user_id):
    categorizacion = db["categorizacion"]
    
    if not categorizacion.find_one({"id_usuario": user_id}):
        print(f"No se encontró categorización para el usuario con ID {user_id}.")
        return

    result = categorizacion.delete_one({"id_usuario": user_id})
    if result.deleted_count > 0:
        print(f"Categorización del usuario con ID {user_id} eliminada correctamente")

# --- Funciones de Autenticación y Sesiones ---
def login(email, password):
    usuarios = db["usuarios"]
    user = usuarios.find_one({"email": email, "password": password})
    if not user:
        print("Credenciales incorrectas.")
        return None
    
    session_key = f"session:{user['id']}"
    redis_client.set(session_key, user['id'])
    print(f"Usuario {user['id']} ha iniciado sesión.")
    return user['id']

def logout(user_id):
    session_key = f"session:{user_id}"
    if redis_client.exists(session_key):
        redis_client.delete(session_key)
        print(f"Usuario {user_id} ha cerrado sesión.")
    else:
        print("No hay sesión activa para este usuario.")

def get_session(user_id):
    session_key = f"session:{user_id}"
    if redis_client.exists(session_key):
        print(f"Sesión activa para el usuario {user_id}.")
        return True
    print("No hay sesión activa.")
    return False

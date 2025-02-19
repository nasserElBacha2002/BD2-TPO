from mongo import connect_mongodb

# --- Funciones de Usuarios ---
def create_user(email, password, user_id, cantidad_compras):
    db = connect_mongodb()
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
    db = connect_mongodb()
    usuarios = db["usuarios"]
    return usuarios.find_one({"id": user_id})

# --- Funciones de Categorización ---
def create_categoria(user_id, categoria):
    db = connect_mongodb()
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
    db = connect_mongodb()
    categorizacion = db["categorizacion"]
    return categorizacion.find_one({"id_usuario": user_id})

def update_categoria_automatica(user_id):
    user = get_user_by_id(user_id)
    if user:
        cantidad_compras = user["cantidad_compras"]
        categoria = "LOW" if cantidad_compras <= 5 else "MEDIUM" if cantidad_compras <= 10 else "TOP"
        create_categoria(user_id, categoria)

# --- Funciones de Productos ---
def create_producto(nombre, descripcion, producto_id):
    db = connect_mongodb()
    productos = db["productos"]
    
    if productos.find_one({"id": producto_id}):
        print(f"El producto con ID {producto_id} ya existe.")
        return

    result = productos.insert_one({"id": producto_id, "nombre": nombre, "descripcion": descripcion})
    print(f"Producto creado con ID: {result.inserted_id}")

def get_producto_by_id(producto_id):
    db = connect_mongodb()
    productos = db["productos"]
    return productos.find_one({"id": producto_id})

def update_producto(producto_id, nombre=None, descripcion=None):
    db = connect_mongodb()
    productos = db["productos"]
    
    update_data = {}
    if nombre:
        update_data["nombre"] = nombre
    if descripcion:
        update_data["descripcion"] = descripcion

    result = productos.update_one({"id": producto_id}, {"$set": update_data})
    if result.modified_count > 0:
        print(f"Producto con ID {producto_id} actualizado correctamente")
    else:
        print(f"No se realizaron cambios en el producto con ID {producto_id}")

def delete_producto(producto_id):
    db = connect_mongodb()
    productos = db["productos"]
    
    result = productos.delete_one({"id": producto_id})
    if result.deleted_count > 0:
        print(f"Producto con ID {producto_id} eliminado correctamente")

def delete_categoria(user_id):
    db = connect_mongodb()
    categorizacion = db["categorizacion"]
    
    result = categorizacion.delete_one({"id_usuario": user_id})
    if result.deleted_count > 0:
        print(f"Categorización del usuario con ID {user_id} eliminada correctamente")

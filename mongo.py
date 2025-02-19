from pymongo import MongoClient

def create_db():
    client = MongoClient("mongodb://localhost:27017/")
    db = client["ecommerce_db"]
    
    # Crear índices para mejorar búsquedas
    db.usuarios.create_index("id", unique=True)
    db.productos.create_index("id", unique=True)
    db.categorizacion.create_index("id_usuario", unique=True)
    
    print(f"Base de datos creada: {db.name}")

def connect_mongodb():
    client = MongoClient("mongodb://localhost:27017/")
    db = client["ecommerce_db"]
    return db

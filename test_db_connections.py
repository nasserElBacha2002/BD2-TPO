from pymongo import MongoClient
import redis
from cassandra.cluster import Cluster

def test_mongo():
    try:
        client = MongoClient("mongodb://localhost:27017/")
        db = client.admin  # Intentamos acceder a la base de administración
        db.command("ping")  # Comando para verificar conexión
        print("✅ Conexión a MongoDB exitosa")
    except Exception as e:
        print(f"❌ Error en MongoDB: {e}")

def test_redis():
    try:
        r = redis.Redis(host='localhost', port=6379, decode_responses=True)
        r.ping()  # Verifica conexión enviando un "ping"
        print("✅ Conexión a Redis exitosa")
    except Exception as e:
        print(f"❌ Error en Redis: {e}")

def test_cassandra():
    try:
        # Usar la forma correcta para pasar las IPs
        cluster = Cluster(["127.0.0.1"], port=9042)  
        session = cluster.connect()  # Crear una sesión
        print("✅ Conexión a Cassandra exitosa")
        cluster.shutdown()  # Cerrar la conexión
    except Exception as e:
        print(f"❌ Error en Cassandra: {e}")

if __name__ == "__main__":
    test_mongo()
    test_redis()
    test_cassandra()

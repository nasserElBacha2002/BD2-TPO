from pymongo import MongoClient
from cassandra.cluster import Cluster
import redis

# --- MongoDB ---
def delete_mongo_data():
    client = MongoClient('mongodb://localhost:27017/')
    for db_name in client.list_database_names():
        if db_name != "admin" and db_name != "local":
            db = client[db_name]
            db.drop_database()
            print(f"Borrada la base de datos MongoDB: {db_name}")

# --- Cassandra ---
def delete_cassandra_data():
    cluster = Cluster(['127.0.0.1'])
    session = cluster.connect()
    keyspaces = session.execute("DESCRIBE KEYSPACES")
    
    for row in keyspaces:
        keyspace = row.keyspace
        print(f"Borrando tablas en el keyspace Cassandra: {keyspace}")
        
        tables = session.execute(f"DESCRIBE TABLES IN {keyspace}")
        
        for table in tables:
            session.execute(f"DROP TABLE IF EXISTS {keyspace}.{table}")
            print(f"Tabla {table} borrada en Cassandra")
    
    cluster.shutdown()

# --- Redis ---
def delete_redis_data():
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    keys = r.keys('*')
    
    for key in keys:
        r.delete(key)
        print(f"Clave {key} borrada de Redis")

# Ejecutar las funciones
#delete_mongo_data()
#delete_cassandra_data()
delete_redis_data()


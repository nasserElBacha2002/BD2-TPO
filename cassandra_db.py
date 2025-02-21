from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from cassandra import DriverException

def connect_cassandra():
    
    try:
        cluster = Cluster(['127.0.0.1'])
        session = cluster.connect('tu_keyspace')  # Conectar directamente al keyspace
        #print("✅ Conexión a Cassandra establecida con el keyspace 'tu_keyspace'.")
        return session
    except Exception as e:
        print(f"❌ Error al conectar a Cassandra: {e}")
        return None
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from cassandra import DriverException

def connect_cassandra():
    try:
        # Configuración del clúster (agrega autenticación si es necesario)
        cluster = Cluster(['127.0.0.1'])  # IP del nodo Cassandra
        session = cluster.connect()
        session.set_keyspace('tu_keyspace')
        print("Conexión a Cassandra exitosa.")

        return session
    except DriverException as e:
        print(f"Error al conectar con Cassandra: {e}")
        return None
    except Exception as e:
        print(f"Error inesperado: {e}")
        return None
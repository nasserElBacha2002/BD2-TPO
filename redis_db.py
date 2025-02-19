import redis

def connect_redis():
    try:
        client = redis.Redis(host="localhost", port=6379, decode_responses=True)
        print("✅ Conectado a Redis")
        return client
    except Exception as e:
        print(f"❌ Error conectando a Redis: {e}")
        return None

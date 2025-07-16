from dotenv import load_dotenv
import os
import redis

load_dotenv()  

def redis_config_():
    host = os.getenv('REDIS_HOST')
    port = os.getenv('REDIS_PORT')
    username = os.getenv('REDIS_USERNAME')
    password = os.getenv('REDIS_PASSWORD')

    print("Host:", host, "Port:", port)

    if host is None or port is None:
        print("❌ Thiếu REDIS_HOST hoặc REDIS_PORT trong file .env")
        return None

    r = redis.Redis(
        host=host,
        port=int(port),
        decode_responses=True,
        username=username,
        password=password
    )
    return r



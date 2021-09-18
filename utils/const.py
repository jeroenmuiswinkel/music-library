TESTING = True

DB_HOST = "localhost" if TESTING else "172.17.0.2"
DB_USER = "admin"
DB_PASSWORD = "s3cret"
DB_NAME = "music-db"
DB_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

REDIS_HOST = "localhost" if TESTING else "172.17.0.3"

REDIS_URL = f"redis://{REDIS_HOST}"

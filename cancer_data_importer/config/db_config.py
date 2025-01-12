import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_CONFIG = {
    'dbname': os.getenv(''),
    'user': os.getenv(''),
    'password': os.getenv(''),
    'host': os.getenv(''),
    'port': os.getenv('')
}

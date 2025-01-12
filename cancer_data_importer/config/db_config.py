import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_CONFIG = {
    'dbname': os.getenv('Cancerdata'),
    'user': os.getenv('POSTGRES_USER'),
    'password': os.getenv('wnghks12!!'),
    'host': os.getenv('localhost'),
    'port': os.getenv('5432')
}

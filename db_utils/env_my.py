import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv('.env', raise_error_if_not_found=False))
print(os.getenv('POSTGRES_USER'))

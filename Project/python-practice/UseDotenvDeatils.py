import os
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env

ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")
print(f"ADMIN_EMAIL: {ADMIN_EMAIL}")



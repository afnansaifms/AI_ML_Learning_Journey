import os
from dotenv import load_dotenv

load_dotenv()
class Settings:
    origins=os.getenv("ORIGINS")

settings = Settings()
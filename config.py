import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
INSTANCE_DIR = BASE_DIR / "instance"

class Config:
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{INSTANCE_DIR / "data.db"}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # DEBUG = True
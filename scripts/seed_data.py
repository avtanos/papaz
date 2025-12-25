"""
Алиас для init_db.py - более понятное имя для заполнения данными
"""
from scripts.init_db import init_db
import sys

if __name__ == "__main__":
    clear = "--clear" in sys.argv or "-c" in sys.argv
    init_db(clear_existing=clear)


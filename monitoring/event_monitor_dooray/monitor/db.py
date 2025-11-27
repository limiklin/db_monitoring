# 데이터베이스 접속

import mariadb
from config.settings import DB_CONFIG

def get_connection():
    try:
        conn = mariadb.connect(
            host=DB_CONFIG["host"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            database=DB_CONFIG["database"],
            port=DB_CONFIG["port"]
        )
        return conn
    except mariadb.Error as e:
        print(f"MariaDB 연결 실패: {e}")
        raise

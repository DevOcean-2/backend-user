import os
from dotenv import load_dotenv
from fastapi import HTTPException
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sshtunnel import SSHTunnelForwarder
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database

load_dotenv()

Base = declarative_base()

class DatabaseManager:
    def __init__(self):
        self.engine = None
        self.SessionLocal = None
        self.Base = Base
        self.server = None
        
    def init_db(self):
        """데이터베이스 및 SSH 터널 초기화"""
        DATABASE_URL = os.getenv("DATABASE_URL")
        if os.getenv("ENV") == "local-dev":
            ssh_host = os.getenv("SSH_HOST")
            ssh_user = os.getenv("SSH_USER")
            db_host = os.getenv("DB_HOST")
            db_port = os.getenv("DB_PORT")

            current_dir = os.path.dirname(os.path.abspath(__file__))
            ssh_key = os.path.join(current_dir, os.getenv("SSH_KEY"))
            self.server = SSHTunnelForwarder(
                (ssh_host, 22),
                ssh_username=ssh_user,
                ssh_pkey=ssh_key,
                remote_bind_address=(db_host, int(db_port)),
                local_bind_address=('127.0.0.1', 5432),
            )
            try:
                self.server.start()  # SSH 터널 시작
                print("SSH Tunnel established")
            except Exception as e:
                print(f"Error establishing SSH tunnel: {e}")
                raise e
        
        self.engine = create_engine(DATABASE_URL)
        if not database_exists(self.engine.url):
            create_database(self.engine.url)
            print("Database created!")
        else:
            print("Database already exists.")
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        
    def cleanup(self):
        """리소스 정리"""
        if self.server and self.server.is_active:
            self.server.stop()
            print("SSH Tunnel closed")
        
    def create_tables(self):
        """데이터베이스 테이블 생성"""
        if not self.engine:
            raise Exception("Database not initialized. Call init_db() first.")
        self.Base.metadata.create_all(bind=self.engine)

db_manager = DatabaseManager()

# Dependency
def get_db():
    if not db_manager.SessionLocal:
        raise Exception("Database not initialized. Call init_db() first.")
    db = db_manager.SessionLocal()
    try:
        yield db
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()
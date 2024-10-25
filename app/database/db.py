import atexit
import os
from dotenv import load_dotenv
from fastapi import HTTPException
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sshtunnel import SSHTunnelForwarder
from sqlalchemy import create_engine
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if os.getenv("ENV") == "local-dev":
    ssh_host = os.getenv("SSH_HOST")
    ssh_user = os.getenv("SSH_USER")
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")

    current_dir = os.path.dirname(os.path.abspath(__file__))
    ssh_key = os.path.join(current_dir, os.getenv("SSH_KEY"))
    server = SSHTunnelForwarder(
        (ssh_host, 22),
        ssh_username=ssh_user,
        ssh_pkey=ssh_key,
        remote_bind_address=(db_host, int(db_port)),
        local_bind_address=('127.0.0.1', 6543),
    )
    try:
        server.start()  # SSH 터널 시작
        print("SSH Tunnel established")
    except Exception as e:
        print(f"Error establishing SSH tunnel: {e}")
    atexit.register(server.stop)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()
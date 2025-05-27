from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# 创建数据库引擎
DATABASE_URL = "mysql+mysqlconnector://root:li040214@localhost/stray_animal_adoption"
engine = create_engine(DATABASE_URL, echo=True)

# 创建 session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_session():
    db_session = SessionLocal()
    try:
        return db_session
    except:
        db_session.close()
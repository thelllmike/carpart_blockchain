from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# MySQL Database connection string
# DATABASE_URL = "mysql+pymysql://username:password@localhost/parking_system"
DATABASE_URL = "mysql+mysqlconnector://root:1234@localhost:3306/carparking"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

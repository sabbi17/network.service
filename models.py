from sqlalchemy import Boolean, Column, Integer, String
from database import Base

class service_app(Base):
    __tablename__ = "Information"

    id = Column(Integer, primary_key=True, index=True)
    zipcode = Column(String, unique=True)
    city = Column(String)
    price = Column(Integer)
    category = Column(String)



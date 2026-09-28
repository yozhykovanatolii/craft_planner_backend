from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime

class Base(DeclarativeBase):
    id = Column(Integer, primary_key=True)

class User(Base):
    __tablename__ = 'users'
    
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    avatar_url = Column(String, nullable=False)
    
    
class CraftPlan(Base):
    __tablename__ = 'craft_plans'
    
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    target_item_name = Column(String, nullable=False)
    target_item_quantity = Column(Integer, nullable=False)
    available_ingredients = Column(JSONB, nullable=False)
    ingredients_to_craft = Column(JSONB, nullable=False)
    required_components = Column(JSONB, nullable=False)
    status = Column(String, default = 'Active')
    created_at = Column(DateTime, default = datetime.now)
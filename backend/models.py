from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from .database import Base

class FavoriteItem(Base):
    __tablename__ = "favorite_items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    type = Column(String)  # movie, book, game
    description = Column(String)
    external_id = Column(String)
    poster_path = Column(String)
    rating = Column(Float)
    status = Column(String)  # watching, completed, plan_to_watch
    notes = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now()) 
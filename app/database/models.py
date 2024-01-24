from sqlalchemy import Column, Integer, String, Boolean, Text, DateTime, Float, JSON
from typing import List
from app.database.session import Base


class PetfinderAnimal(Base):
    __tablename__ = "petfinder_animals"

    id = Column(Integer, primary_key=True, index=True)
    response_data = Column(JSON)
    type = Column(String, nullable=True)
    breed = Column(String, nullable=True)
    size = Column(String, nullable=True)
    gender = Column(String, nullable=True)
    age = Column(String, nullable=True)
    color = Column(String, nullable=True)
    coat = Column(String, nullable=True)
    status = Column(String, nullable=True)
    name = Column(String, nullable=True)
    organization = Column(String, nullable=True)
    good_with_children = Column(Boolean, nullable=True)
    good_with_dogs = Column(Boolean, nullable=True)
    good_with_cats = Column(Boolean, nullable=True)
    house_trained = Column(Boolean, nullable=True)
    declawed = Column(Boolean, nullable=True)
    special_needs = Column(Boolean, nullable=True)
    location = Column(String, nullable=True)
    distance = Column(Integer, default=100)
    before = Column(String, nullable=True)
    after = Column(String, nullable=True)
    sort = Column(String, default="recent")
    page = Column(Integer, default=1)
    limit = Column(Integer, default=20)

from sqlalchemy import Column, Integer, String, Boolean, Text, DateTime, Float, JSON
from typing import List, Optional, Any
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship



class Base(DeclarativeBase):
    type_annotation_map = {dict[str, Any]: JSON}


class PetfinderAnimals(Base):
    __tablename__ = "petfinder_animals"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    response_data: Mapped[dict[str, Any]]
    type: Mapped[Optional[str]]
    breed: Mapped[Optional[List[str]]]
    size: Mapped[Optional[List[str]]]
    gender: Mapped[Optional[List[str]]]
    age: Mapped[Optional[List[str]]]
    color: Mapped[Optional[str]]
    coat: Mapped[Optional[List[str]]]
    status: Mapped[Optional[List[str]]]
    name: Mapped[Optional[str]]
    organization: Mapped[Optional[List[str]]]
    good_with_children: Mapped[Optional[bool]]
    good_with_dogs: Mapped[Optional[bool]]
    good_with_cats: Mapped[Optional[bool]]
    house_trained: Mapped[Optional[bool]]
    declawed: Mapped[Optional[bool]]
    special_needs: Mapped[Optional[bool]]
    location: Mapped[Optional[str]]
    distance: Mapped[int] = mapped_column(Integer, default=100)
    before: Mapped[Optional[str]]
    after: Mapped[Optional[str]]
    sort: Mapped[Optional[str]] = mapped_column(String, default="recent")
    page: Mapped[int] = mapped_column(Integer, default=1)
    limit: Mapped[int] = mapped_column(Integer, default=20)

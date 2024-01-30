from sqlalchemy import Column, Integer, String, Boolean, Text, DateTime, Float, JSON
from typing import List, Optional, Any
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import ARRAY, JSONB
from sqlmodel import SQLModel, Field, JSON



# class Base(DeclarativeBase):
#     type_annotation_map = {dict[str, Any]: JSON}


# class PetfinderAnimalsDataDump(Base):
#     __tablename__ = "petfinder_animals"

#     id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
#     response_data: Mapped[dict[str, Any]]
#     type: Mapped[Optional[str]]
#     breed: Mapped[Optional[List[str]]] = mapped_column(ARRAY(String))
#     size: Mapped[Optional[List[str]]] = mapped_column(ARRAY(String))
#     gender: Mapped[Optional[List[str]]] = mapped_column(ARRAY(String))
#     age: Mapped[Optional[List[str]]] = mapped_column(ARRAY(String))
#     color: Mapped[Optional[str]]
#     coat: Mapped[Optional[List[str]]] = mapped_column(ARRAY(String))
#     status: Mapped[Optional[List[str]]] = mapped_column(ARRAY(String))
#     name: Mapped[Optional[str]]
#     organization: Mapped[Optional[List[str]]] = mapped_column(ARRAY(String))
#     good_with_children: Mapped[Optional[bool]]
#     good_with_dogs: Mapped[Optional[bool]]
#     good_with_cats: Mapped[Optional[bool]]
#     house_trained: Mapped[Optional[bool]]
#     declawed: Mapped[Optional[bool]]
#     special_needs: Mapped[Optional[bool]]
#     location: Mapped[Optional[str]]
#     distance: Mapped[int] = mapped_column(Integer, default=100)
#     before: Mapped[Optional[str]]
#     after: Mapped[Optional[str]]
#     sort: Mapped[Optional[str]] = mapped_column(String, default="recent")
#     page: Mapped[int] = mapped_column(Integer, default=1)
#     limit: Mapped[int] = mapped_column(Integer, default=20)


class PetfinderAnimalsDataDump(SQLModel, table=True):
    __tablename__ = "petfinder_animals"

    id: int = Field(primary_key=True, index=True)
    response_data: JSON = Field(sa_column=Column(JSONB))
    type: Optional[str]
    breed: Optional[List[str]]
    size: Optional[List[str]]
    gender: Optional[List[str]]
    age: Optional[List[str]]
    color: Optional[str]
    coat: Optional[List[str]]
    status: Optional[List[str]]
    name: Optional[str]
    organization: Optional[List[str]]
    good_with_children: Optional[bool]
    good_with_dogs: Optional[bool]
    good_with_cats: Optional[bool]
    house_trained: Optional[bool]
    declawed: Optional[bool]
    special_needs: Optional[bool]
    location: Optional[str]
    distance: int = Field(default=100)
    before: Optional[str]
    after: Optional[str]
    sort: Optional[str] = Field(default="recent")
    page: int = Field(default=1)
    limit: int = Field(default=20)

    class Config:
        arbitrary_types_allowed = True
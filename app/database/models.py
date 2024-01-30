from typing import List, Optional, Any, Dict
from sqlmodel import SQLModel, Field
from sqlmodel import JSON as sqlmodel_json
from sqlalchemy import Column, String, ARRAY
from sqlalchemy.dialects.postgresql import JSONB
from app.get_petfinder_data.models import GetPetFinderDataRequest



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
    response_data: GetPetFinderDataRequest = Field(sa_column=Column(JSONB))
    type: Optional[str] = None
    breed: Optional[List[str]] = Field(sa_column=Column(ARRAY(String)))
    size:  Optional[List[str]] = Field(sa_column=Column(ARRAY(String)))
    gender: Optional[List[str]] = Field(sa_column=Column(ARRAY(String)))
    age: Optional[List[str]] = Field(sa_column=Column(ARRAY(String)))
    color: Optional[str] = None
    coat: Optional[List[str]] = Field(sa_column=Column(ARRAY(String)))
    status: Optional[List[str]] = Field(sa_column=Column(ARRAY(String)))
    name: Optional[str] = None
    organization: Optional[list[str]] = Field(sa_column=Column(ARRAY(String)))
    good_with_children: Optional[bool] = None
    good_with_dogs: Optional[bool] = None
    good_with_cats: Optional[bool] = None
    house_trained: Optional[bool] = None
    declawed: Optional[bool] = None
    special_needs: Optional[bool] = None
    location: Optional[str] = None
    distance: int = 100
    before: Optional[str] = None
    after: Optional[str] = None
    sort: Optional[str] = "recent"
    page: int = 1
    limit: int = 20

    class Config:
        arbitrary_types_allowed = True
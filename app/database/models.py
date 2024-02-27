from typing import List, Optional, Any, Dict
from pydantic import BaseModel
# from datetime import datetime
from sqlmodel import SQLModel, Field, Column, String, ARRAY, Relationship, Integer
from sqlalchemy.dialects.postgresql import JSONB



"""
Data Dump table and models
"""
class PetfinderAnimalsDataDump(SQLModel, table=True):
    __tablename__ = "petfinder_animals_raw"

    id: int = Field(primary_key=True, index=True)
    request_batch_id: int = Field(index=True)
    page: int = 1
    limit: int = 20
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
    response_data: Dict = Field(sa_column=Column(JSONB))

    # animals: Optional[List["Animal"]] = Relationship(back_populates="petfinder_animals_data_dump")
         
    class Config:
        arbitrary_types_allowed = True


class PetfinderAnimalsDataDumpResponse(BaseModel):
    id: int
    request_batch_id: int
    page: int
    limit: int
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
    distance: int
    before: Optional[str]
    after: Optional[str]
    sort: Optional[str]
         
    class Config:
        arbitrary_types_allowed = True



"""
Animals table and models
"""
class Animal(SQLModel, table=True):
    __tablename__ = "animals"

    id: int = Field(primary_key=True, index=True)
    petfinder_id: int = Field(index=True)
    organization_id: Optional[str]
    url: Optional[str]
    type: Optional[str] = Field(index=True)
    species: Optional[str] = Field(index=True)
    breeds_primary: Optional[str]
    breeds_secondary: Optional[str]
    breeds_mixed: Optional[bool]
    breeds_unknown: Optional[bool]
    colors_primary: Optional[str]
    colors_secondary: Optional[str]
    colors_tertiary: Optional[str]
    age: Optional[str]
    gender: Optional[str]
    size: Optional[str]
    coat: Optional[str]
    # # attributes
    spayed_neutered: Optional[bool]
    house_trained: Optional[bool]
    declawed: Optional[bool]
    special_needs: Optional[bool]
    shots_current: Optional[bool]
    # # environment
    good_with_children: Optional[bool]
    good_with_dogs: Optional[bool]
    good_with_cats: Optional[bool]
    tags: Optional[List[str]] = Field(sa_column=Column(ARRAY(String)))
    name: Optional[str] = Field(index=True)
    description: Optional[str]
    organization_animal_id: Optional[str]
    # # photos: List[str]
    # photo_small: Optional[str]
    # photo_medium: Optional[str]
    # photo_large: Optional[str]
    # photo_full: Optional[str]
    primary_photo_cropped_small: Optional[str]
    primary_photo_cropped_medium: Optional[str]
    primary_photo_cropped_large: Optional[str]
    primary_photo_cropped_full: Optional[str]
    # # videos: List[str]
    status: Optional[str]
    status_changed_at: Optional[str]
    published_at: Optional[str]
    distance: Optional[float]
    # # contact
    email: Optional[str]
    phone: Optional[str]
    # # address = Address
    address1: Optional[str]
    address2: Optional[str]
    city: Optional[str]
    state: Optional[str]
    postcode: Optional[str]
    country: Optional[str]

    # petfinder_animals_data_dump_id: int = Field(default=None, foreign_key="petfinder_animals_data_dump.id")
    # petfinder_animals_data_dump: [PetfinderAnimalsDataDump] = Relationship(back_populates="animals")


"""
PetNameGame tables and models
"""
class CardBoardLink(SQLModel, table=True):
    card_id: Optional[int] = Field(default=None, foreign_key="animal_cards.id", primary_key=True)
    board_id: Optional[int] = Field(default=None, foreign_key="game_boards.id", primary_key=True)


class AnimalCard(SQLModel, table=True):
    __tablename__ = "animal_cards"

    id: int = Field(primary_key=True, index=True)
    petfinder_id: int = Field(index=True)
    type: Optional[str]
    name: Optional[str]
    gender: Optional[str]
    primary_photo_cropped_medium: Optional[str]

    # game_board: Optional["GameBoard"] = Relationship(back_populates="animals", link_model=CardBoardLink)


class GameBoard(SQLModel, table=True):
    __tablename__ = "game_boards"

    id: int = Field(primary_key=True, index=True)
    game_type: Optional[str] = None
    animal_type: Optional[str] = None
    gender: Optional[str] = None
    # answer: Optional[List[AnimalCard]] = Field(sa_column=Column(ARRAY(AnimalCard)))

    # animals: List[AnimalCard] = Relationship(back_populates="game_board", link_model=CardBoardLink)

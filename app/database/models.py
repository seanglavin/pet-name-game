from typing import List, Optional, Any, Dict
from sqlmodel import SQLModel, Field, Column, String, ARRAY
# from sqlalchemy import Column, String, ARRAY
from sqlalchemy.dialects.postgresql import JSONB



class PetfinderAnimalsDataDump(SQLModel, table=True):
    __tablename__ = "petfinder_animals"

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
         
    class Config:
        arbitrary_types_allowed = True


class PetfinderAnimalsDataDumpResponse(SQLModel):
    id: int
    request_batch_id: int = Field(index=True)
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


class ResponseDataRead(SQLModel):
    id: int
    response_data: Dict = Field(sa_column=Column(JSONB))
         
    class Config:
        arbitrary_types_allowed = True
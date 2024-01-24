from pydantic import BaseModel
from typing import List, Optional

class GetPetFinderDataRequest(BaseModel):
    type: Optional[str] = None
    breed: Optional[List[str]] = None
    size: Optional[List[str]] = None
    gender: Optional[List[str]] = None
    age: Optional[List[str]] = None
    color: Optional[str] = None
    coat: Optional[List[str]] = None
    status: Optional[List[str]] = None
    name: Optional[str] = None
    organization: Optional[List[str]] = None
    good_with_children: Optional[bool] = None
    good_with_dogs: Optional[bool] = None
    good_with_cats: Optional[bool] = None
    house_trained: Optional[bool] = None
    declawed: Optional[bool] = None
    special_needs: Optional[bool] = None
    location: Optional[str] = None
    distance: Optional[int] = 100
    before: Optional[str] = None
    after: Optional[str] = None
    sort: Optional[str] = "recent"
    page: Optional[int] = 1
    limit: Optional[int] = 20

    def flatten_params(self):
        return self.model_dump(exclude_unset=True)

    class Config:
        json_schema_extra = {
            "example": {
                "type": "cat", #
                "breed": ["pug", "samoyed"], # Accepts multiple values, e.g. breed=pug,samoyed.
                "size": ["large", "xlarge"], # small, medium, large, xlarge Accepts multiple values, e.g. size=large,xlarge.
                "gender": ["male", "female"], # male, female, unknown Accepts multiple values, e.g. gender=male,female.
                "age": ["baby", "senior"], # baby, young, adult, senior Accepts multiple values, e.g. age=baby,senior.
                "color": "white", #
                "coat": ["short", "medium"], # short, medium, long, wire, hairless, curly Accepts multiple values, e.g. coat=wire,curly
                "status": ["adoptable"], # adoptable, adopted, found Accepts multiple values (default: adoptable)
                "name": "Fluffy", # Return results matching animal name (includes partial matches; e.g. "Fred" will return "Alfredo" and "Frederick")
                "organization": ["ID1", "ID2"], #
                "good_with_children": True, # Can be true, false, 1, or 0
                "good_with_dogs": True, # Can be true, false, 1, or 0
                "good_with_cats": False, # Can be true, false, 1, or 0
                "house_trained": True, # Can be true or 1 only
                "declawed": False, # Can be true or 1 only
                "special_needs": False, # Can be true or 1 only
                "location": "New York, NY", # Example: city, state/province; or postal code
                "distance": 50, # Requires location to be set, max: 500, measured in miles
                "before": "2023-01-01T00:00:00+00:00", # ISO8601
                "after": "2022-01-01T00:00:00+00:00", # ISO8601
                "sort": "recent", # recent, -recent, distance, -distance, random
                "page": 1, #
                "limit": 20 # Max: 100
            }
        }
    
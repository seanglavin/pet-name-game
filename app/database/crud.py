# from sqlalchemy import text
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import HTTPException
from app.database.models import PetfinderAnimalsDataDump
from app.get_petfinder_data.models import GetPetFinderDataRequest
from sqlalchemy.orm import load_only
from sqlmodel import select, text


async def get_largest_request_batch_id(db: AsyncSession) -> int:
    """
    
    """
    largest_batch_number = 0
    statement = select(PetfinderAnimalsDataDump.request_batch_id).order_by(PetfinderAnimalsDataDump.request_batch_id.desc()).limit(1)
    results = await db.exec(statement)
    if results is not None:
        result = results.first()
        if result is not None:
            largest_batch_number = result[0]
    return largest_batch_number

async def save_petfinder_data(db: AsyncSession, response_data: dict, request: GetPetFinderDataRequest, request_batch_id: int):
    """
    Save Petfinder data (API response and request parameters) to the database.

    Args:
        db: SQLAlchemy database session.
        response_data: Response data from Petfinder API.
        request: Request parameters used to query the Petfinder API.
    """
    # Create a new PetfinderAnimalsDataDump instance
    petfinder_animals_dump = PetfinderAnimalsDataDump(
        type=request.type,
        breed=request.breed,
        size=request.size,
        gender=request.gender,
        age=request.age,
        color=request.color,
        coat=request.coat,
        status=request.status,
        name=request.name,
        organization=request.organization,
        good_with_children=request.good_with_children,
        good_with_dogs=request.good_with_dogs,
        good_with_cats=request.good_with_cats,
        house_trained=request.house_trained,
        declawed=request.declawed,
        special_needs=request.special_needs,
        location=request.location,
        distance=request.distance,
        before=request.before,
        after=request.after,
        sort=request.sort,
        request_batch_id=request_batch_id,
        page=request.page,
        limit=request.limit,
        response_data=response_data
    )

    # Add the new PetfinderAnimalsDataDump instance to the session and commit the transaction
    db.add(petfinder_animals_dump)
    await db.commit()
    await db.refresh(petfinder_animals_dump)
    return petfinder_animals_dump


async def get_petfinder_animals(db: AsyncSession):
    """
    Retrieve PetfinderAnimalsDataDump from the database.

    Args:
        db: SQLAlchemy database session.
        limit: Maximum number of records to retrieve.

    Returns:
        List of PetfinderAnimalsDataDumpResponse objects.
    """
    statement = select(PetfinderAnimalsDataDump)
    results = await db.exec(statement)
    if results:
        data_dumps = results.all()
        serialized_data_dumps = [dump.model_dump() for dump in data_dumps]
        return serialized_data_dumps
    return None


async def get_response_data_by_dump_id(petfinder_animals_data_dump_id: int, db: AsyncSession):
    """
    Retrieve response data from the saved PetfinderAnimalsDataDump.

    Args:
        db: SQLAlchemy database session.
        petfinder_animals_data_dump_id: ID of the PetfinderAnimalsDataDump object.

    Returns:
        List of Animals for specified data dump id
    """
    try:
        statement = select(PetfinderAnimalsDataDump).where(PetfinderAnimalsDataDump.id == petfinder_animals_data_dump_id)
        results = await db.exec(statement)

        if results:
            data = results.first()
            response_data = data.response_data.get("animals", [])
            return response_data
        else:
            raise HTTPException(status_code=404, detail=f"No animals found for data dump id: {petfinder_animals_data_dump_id}")
        
    except Exception as e:
        raise e


async def get_response_data_by_batch_id(petfinder_animals_batch_id: int, db: AsyncSession):
    """
    Retrieve response data from the saved PetfinderAnimalsDataDump.

    Args:
        db: SQLAlchemy database session.
        request_batch_id: ID of the PetfinderAnimalsDataDump batch of objects.

    Returns:
        List of Animals for specified data dump id
    """
    try:
        statement = select(PetfinderAnimalsDataDump).where(PetfinderAnimalsDataDump.request_batch_id == petfinder_animals_batch_id)
        results = await db.exec(statement)

        batched_animals = []

        for result in results:
            response_data = result.response_data.get("animals", [])

            for animal in response_data:
                batched_animals.append(animal)

        if batched_animals:
            return batched_animals
        else:
            raise HTTPException(status_code=404, detail=f"No animals found for data dump id: {petfinder_animals_batch_id}")
        
    except Exception as e:
        raise e



async def delete_all_petfinder_data(db: AsyncSession):
    """
    Delete all entries in the PetFinderAnimalsDataDump table petfinder_animals.

    Args:
        db: SQLAlchemy database session.

    Returns:
        # of rows deleted
    """
    result = await db.exec(PetfinderAnimalsDataDump.__table__.delete())
    await db.exec(text("ALTER SEQUENCE petfinder_animals_id_seq RESTART WITH 1"))
    await db.commit()
    return result.rowcount
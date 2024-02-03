# from sqlalchemy import text
from sqlmodel.ext.asyncio.session import AsyncSession
from app.database.models import PetfinderAnimalsDataDump
from app.get_petfinder_data.models import GetPetFinderDataRequest
from sqlalchemy.orm import load_only
from sqlmodel import select, text

async def save_petfinder_data(db: AsyncSession, response_data: dict, request: GetPetFinderDataRequest):
    """
    Save Petfinder data (API response and request parameters) to the database.

    Args:
        db: SQLAlchemy database session.
        response_data: Response data from Petfinder API.
        request: Request parameters used to query the Petfinder API.
    """
    # Create a new PetfinderAnimalsDataDump instance
    petfinder_animals_dump = PetfinderAnimalsDataDump(
        response_data=response_data,
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
        page=request.page,
        limit=request.limit
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


async def get_response_data(petfinder_animals_data_dump_id: int, db: AsyncSession):
    """
    Retrieve response data from the saved PetfinderAnimalsDataDump.

    Args:
        db: SQLAlchemy database session.
        petfinder_animals_data_dump_id: ID of the PetfinderAnimalsDataDump object.

    Returns:
        Dictionary containing response data.
    """
    statement = select(PetfinderAnimalsDataDump).where(PetfinderAnimalsDataDump.id == petfinder_animals_data_dump_id)
    results = await db.exec(statement)
    if results:
        data = results.all()
        return data[0].response_data
        # serialized_response_datas = [dump.model_dump() for dump in response_data]
        # return serialized_response_datas
    return None


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
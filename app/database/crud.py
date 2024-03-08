# from sqlalchemy import text
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import HTTPException
from app.database.models import PetfinderAnimalsDataDump, Animal, AnimalCard, GameBoard, GameBoardWithAnimals
from app.get_petfinder_data.models import GetPetFinderDataRequest
from sqlmodel import select, text, func, cast, ARRAY, Integer
from typing import List
import json


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
    try:
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
    except Exception as e:
        raise e


async def save_animal(db: AsyncSession, animal_data: dict):
    """
    Save an animal to the database.
    """
    try:
        animal = Animal(
            petfinder_id = animal_data["id"],
            organization_id = animal_data["organization_id"],
            url = animal_data["url"],
            type = animal_data["type"],
            species = animal_data["species"],
            breeds_primary = animal_data["breeds"]["primary"],
            breeds_secondary = animal_data["breeds"]["secondary"],
            breeds_mixed = animal_data["breeds"]["mixed"],
            breeds_unknown = animal_data["breeds"]["unknown"],
            colors_primary = animal_data["colors"]["primary"],
            colors_secondary = animal_data["colors"]["secondary"],
            colors_tertiary = animal_data["colors"]["tertiary"],
            age = animal_data["age"],
            gender = animal_data["gender"],
            size = animal_data["size"],
            coat = animal_data["coat"],
            spayed_neutered = animal_data["attributes"]["spayed_neutered"],
            house_trained = animal_data["attributes"]["house_trained"],
            declawed = animal_data["attributes"]["declawed"],
            special_needs = animal_data["attributes"]["special_needs"],
            shots_current = animal_data["attributes"]["shots_current"],
            good_with_children = animal_data["environment"]["children"],
            good_with_dogs = animal_data["environment"]["dogs"],
            good_with_cats = animal_data["environment"]["cats"],
            tags = animal_data["tags"],
            name = animal_data["name"],
            description = animal_data["description"],
            organization_animal_id = animal_data["organization_animal_id"],
            primary_photo_cropped_small = animal_data["primary_photo_cropped"]["small"] if animal_data["primary_photo_cropped"] else None,
            primary_photo_cropped_medium = animal_data["primary_photo_cropped"]["medium"] if animal_data["primary_photo_cropped"] else None,
            primary_photo_cropped_large = animal_data["primary_photo_cropped"]["large"] if animal_data["primary_photo_cropped"] else None,
            primary_photo_cropped_full = animal_data["primary_photo_cropped"]["full"] if animal_data["primary_photo_cropped"] else None,
            status = animal_data["status"],
            status_changed_at = animal_data["status_changed_at"],
            published_at = animal_data["published_at"],
            distance = animal_data["distance"],
            email = animal_data["contact"]["email"],
            phone = animal_data["contact"]["phone"],
            address1 = animal_data["contact"]["address"]["address1"],
            address2 = animal_data["contact"]["address"]["address2"],
            city = animal_data["contact"]["address"]["city"],
            state = animal_data["contact"]["address"]["state"],
            postcode = animal_data["contact"]["address"]["postcode"],
            country = animal_data["contact"]["address"]["country"],
        )

        db.add(animal)

        await db.commit()
        await db.refresh(animal)
        return animal
    except Exception as e:
        await db.rollback()
        raise e
    

async def save_animal_card(db: AsyncSession, animal_data: dict):
    """
    Save an animal to the database.
    """
    try:
        animal_card = AnimalCard(
            petfinder_id = animal_data["petfinder_id"],
            type = animal_data["type"],
            name = animal_data["name"],
            gender = animal_data["gender"],
            primary_photo_cropped_medium = animal_data["primary_photo_cropped_medium"]
        )

        db.add(animal_card)

        await db.commit()
        await db.refresh(animal_card)
        return animal_card
    except Exception as e:
        await db.rollback()
        raise e
    

async def save_game_boards(db: AsyncSession, game_board_data: List[GameBoard]):
    """
    Save list of GameBards to the database.
    """
    try:
        # bulk insert
        db.add_all(game_board_data)
        await db.commit()
        # no db.refresh() when doing bulk insert.
        # await db.refresh(game_board_data)
        return {"GameBoards loaded: ", len(game_board_data)}
    except Exception as e:
        await db.rollback()
        raise e


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


async def save_animal_from_response_data_by_batch_id(petfinder_animals_batch_id: int, db: AsyncSession):
    """
    Retrieve response data from the saved PetfinderAnimalsDataDump and save it each animal as an entry in Animal table.

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

            for animal_data in response_data:
                batched_animals.append(animal_data)

        if batched_animals:
            for animal in batched_animals:
                await save_animal(db, animal)
            return {"Animals loaded: ", len(batched_animals)}
        else:
            raise HTTPException(status_code=404, detail=f"No animals found for data dump id: {petfinder_animals_batch_id}")
        
    except Exception as e:
        raise e
    

async def get_animals(db: AsyncSession):
    """
    Retrieve PetfinderAnimalsDataDump from the database.

    Args:
        db: SQLAlchemy database session.
        limit: Maximum number of records to retrieve.

    Returns:
        List of PetfinderAnimalsDataDumpResponse objects.
    """
    statement = select(Animal)
    results = await db.exec(statement)
    if results:
        data_dumps = results.all()
        serialized_data_dumps = [dump.model_dump() for dump in data_dumps]
        return serialized_data_dumps
    return None


async def save_animal_cards_from_animals_table(db: AsyncSession):
    """
    Retrieve animals from Animals table and create animal cards if animal has a primary_cropped_photo.

    Args:
        db: SQLAlchemy database session.
        request_batch_id: ID of the PetfinderAnimalsDataDump batch of objects.

    Returns:
        List of Animals for specified data dump id
    """
    try:
        statement = select(Animal).where(Animal.primary_photo_cropped_medium != None)
        result = await db.exec(statement)   # sqlalchemy object

        if result:
            results = result.all() # turns result into list of Animal objects
            serialized_animals = [animal.model_dump() for animal in results] # dumps models into list of dictionaries
            for animal in serialized_animals:
                await save_animal_card(db, animal)
            return {"AnimalCards loaded: ", len(serialized_animals)}

        else:
            raise HTTPException(status_code=404, detail=f"No animals found for with primary_photo_cropped_medium")   
        
    except Exception as e:
        raise e
    

async def get_animal_cards(db: AsyncSession, name: str = None, type: str = None, gender: str = None):
    """
    Retrieve AnimalCard table from the database.

    Args:
        db: SQLAlchemy database session.
        name:   Case insensitive pattern match.
        type:  
                Cat, 
                Dog, 
                Rabbit, 
                Horse, 
                Small & Furry, 
                Bird, 
                Scales, Fins & Other, 
                Barnyard
        gender:
                Male, 
                Female, 
                Unknown
    Returns:
        List of AnimalCard objects.
    """
    try:
        statement = select(AnimalCard)

        if name:
            statement = statement.where(func.lower(AnimalCard.name).ilike(f'%{name.lower()}%'))
        if type:
            statement = statement.where(func.lower(AnimalCard.type) == type.lower())
        if gender:
            statement = statement.where(func.lower(AnimalCard.gender) == gender.lower())

        results = await db.exec(statement)

        animals = results.all()
        serialized_animals = [animal.model_dump() for animal in animals]
        return serialized_animals
    
    except Exception as e:
        print(f"Error retrieving AnimalCards: {e}")
        return None
    

async def get_animal_cards_by_list_of_card_ids(db: AsyncSession, ids: List[int]) -> List[AnimalCard]:
    """
    Retrieve AnimalCard objects by list of card ids.
    """
    try:
        statement = select(AnimalCard).where(AnimalCard.id.in_(ids))
        results = await db.exec(statement)
        return results.all()
    except Exception as e:
        raise e
      

async def test_get_all_game_boards(
    db: AsyncSession,
    id: int = None,
    game_type: str = None,
    animal_type: str = None,
    gender: str = None
    ) -> List[GameBoardWithAnimals]:
    """
    Retrieve GameBoards from game_board table from the database.

    Args:
        db: SQLAlchemy database session.

    Returns:
        List of GameBoard objects.
    """

    try:
        print(GameBoard.animals)
        statement = select(GameBoard, AnimalCard).join(AnimalCard, AnimalCard.id.in_(GameBoard.animals))

        if id is not None:
            statement = statement.where(GameBoard.id == id)
        if game_type is not None:
            statement = statement.where(func.lower(GameBoard.game_type) == game_type.lower())
        if animal_type is not None:
            statement = statement.where(func.lower(GameBoard.animal_type) == animal_type.lower())
        if gender is not None:
            statement = statement.where(func.lower(GameBoard.gender) == gender.lower())

        results = await db.exec(statement)
        game_boards = results.all()

        game_boards_with_animals = []
        for game_board, animal_card in game_boards:
            if game_board.id not in game_boards_with_animals:
                game_boards_with_animals[game_board.id] = GameBoardWithAnimals(**game_board.model_dump(), animals_data=[])
            game_boards_with_animals[game_board.id].animals_data.append(animal_card)

        return game_boards_with_animals
    
    except Exception as e:
        raise e


async def get_all_game_boards(
    db: AsyncSession,
    id: int = None,
    game_type: str = None,
    animal_type: str = None,
    gender: str = None
    ) -> List[GameBoardWithAnimals]:
    """
    Retrieve GameBoards from game_board table from the database.

    Args:
        db: SQLAlchemy database session.

    Returns:
        List of GameBoard objects.
    """

    try: 
        statement = select(GameBoard)
        
        if id is not None:
            statement = statement.where(GameBoard.id == id)
        if game_type is not None:
            statement = statement.where(func.lower(GameBoard.game_type) == game_type.lower())
        if animal_type is not None:
            statement = statement.where(func.lower(GameBoard.animal_type) == animal_type.lower())
        if gender is not None:
            statement = statement.where(func.lower(GameBoard.gender) == gender.lower())

        results = await db.exec(statement.order_by(GameBoard.id.asc()))
        game_boards = results.all()

        all_animal_card_ids = []

        for game_board in game_boards:
            all_animal_card_ids.extend(game_board.animals)

        animal_cards = await get_animal_cards_by_list_of_card_ids(db=db, ids=all_animal_card_ids)
        animal_cards_map = {card.id: card for card in animal_cards}


        game_boards_with_animals = []

        for game_board in game_boards:
            animal_cards_data = {animal_card_id: animal_cards_map[animal_card_id] for animal_card_id in game_board.animals if animal_card_id in animal_cards_map}
            game_board_with_animals = GameBoardWithAnimals(**game_board.model_dump(), animals_data = animal_cards_data)
            game_boards_with_animals.append(game_board_with_animals)

        return game_boards_with_animals
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
    await db.exec(text("ALTER SEQUENCE petfinder_animals_raw_id_seq RESTART WITH 1"))
    await db.commit()
    return result.rowcount


async def delete_all_animal_data(db: AsyncSession):
    """
    Delete all entries in the Animal table animals.

    Args:
        db: SQLAlchemy database session.

    Returns:
        # of rows deleted
    """
    result = await db.exec(Animal.__table__.delete())
    await db.exec(text("ALTER SEQUENCE animals_id_seq RESTART WITH 1"))
    await db.commit()
    return result.rowcount


async def delete_all_animal_cards_data(db: AsyncSession):
    """
    Delete all entries in the AnimalCard table animals.

    Args:
        db: SQLAlchemy database session.

    Returns:
        # of rows deleted
    """
    result = await db.exec(AnimalCard.__table__.delete())
    await db.exec(text("ALTER SEQUENCE animal_cards_id_seq RESTART WITH 1"))
    await db.commit()
    return result.rowcount


async def delete_all_game_boards_data(db: AsyncSession):
    """
    Delete all entries in the GameBoard table.

    Args:
        db: SQLAlchemy database session.

    Returns:
        # of rows deleted
    """
    result = await db.exec(GameBoard.__table__.delete())
    await db.exec(text("ALTER SEQUENCE game_boards_id_seq RESTART WITH 1"))
    await db.commit()
    return result.rowcount
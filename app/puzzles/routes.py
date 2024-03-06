from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from sqlmodel.ext.asyncio.session import AsyncSession
from pydantic import ValidationError
import logging

from app.database.session import get_db
from app.database.models import Animal, AnimalCard, GameBoard, GameBoardWithAnimals
from app.database.crud import get_animal_cards, get_all_game_boards, delete_all_game_boards_data, save_game_boards, test_get_all_game_boards
from app.puzzles.puzzle_maker import game_board_maker


logger = logging.getLogger(__name__)

router = APIRouter(prefix="/puzzles", tags=["puzzles"])


@router.post("/game_boards")
async def create_game_boards(db: AsyncSession = Depends(get_db),
                                 animal_type: Optional[str] = None,
                                 gender: Optional[str] = None,
                                 game_type: Optional[str] = None
                                 ):
    try:
        result = await get_animal_cards(db, name = None, type=animal_type, gender=gender)
        animal_cards = [AnimalCard(**card) for card in result]
        puzzles = await game_board_maker(animal_cards = animal_cards, 
                                         game_type = game_type, 
                                         animal_type = animal_type, 
                                         gender = gender)
        saved_game_boards = await save_game_boards(db, game_board_data = puzzles)
        response = saved_game_boards
        return response
    
    except HTTPException as http_exception:
        raise http_exception
    
    except Exception as e:
        # raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
        raise e
    

# @router.get("/game_boards", response_model=List[GameBoard])
# async def read_all_game_boards(db: AsyncSession = Depends(get_db)):
#     try:
#         result = await get_all_game_boards(db)
#         response = result
#         return response
    
#     except HTTPException as http_exception:
#         raise http_exception
    
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


@router.get("/game_boards", response_model=List[GameBoardWithAnimals])
async def read_all_game_boards(
    db: AsyncSession = Depends(get_db),
    id: Optional[int] = None,
    game_type: Optional[str] = None,
    animal_type: Optional[str] = None,
    gender: Optional[str] = None
    ):
    
    try:
        result = await get_all_game_boards(
            db, id = id, game_type = game_type, animal_type = animal_type, gender = gender
            )
        return result
 
    except HTTPException as http_exception:
        raise http_exception
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}") 


@router.get("/test/game_boards", response_model=List[GameBoardWithAnimals])
async def test_read_all_game_boards(db: AsyncSession = Depends(get_db)):

    try:
        result = await test_get_all_game_boards(db)
        return result
 
    except HTTPException as http_exception:
        raise http_exception
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    






@router.delete("/game_boards")
async def delete_all_game_boards(db: AsyncSession = Depends(get_db)):
    response = await delete_all_game_boards_data(db)
    return {f"Table entries deleted: {response}"}
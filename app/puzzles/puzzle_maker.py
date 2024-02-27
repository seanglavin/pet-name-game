import re
import random
from typing import List
from app.database.models import AnimalCard, GameBoard



async def apply_name_filter(animal_cards: List[AnimalCard]) -> List[AnimalCard]:
    filtered_cards = []

    name_filter_regex = re.compile('^[a-zA-Z ]+$')
    exclude_words_regex = re.compile('(adopt|adoption|adopted|foster|courtesy|needs|needed|friend|partner|bonded|pair|indoor|duo|adult)')

    for card in animal_cards:
        if name_filter_regex.match(card.name) and not exclude_words_regex.search(card.name):
            filtered_cards.append(card)      

    return filtered_cards


async def game_board_maker(animal_cards: List[AnimalCard], game_type: str = None, animal_type: str = None, gender: str = None) -> List[GameBoard]:
    # Step 1: Apply name filter to cards
    filtered_cards = await apply_name_filter(animal_cards)

    random.shuffle(filtered_cards)

    # Step 2: Group and Save Animal Cards to GameBoard
    grouped_cards = [filtered_cards[i:i + 12] for i in range(0, len(filtered_cards), 12)]
    game_boards = []

    for group in grouped_cards:
        answer_cards = random.sample(group, 4)  # Select 4 random cards as the answer
        game_board = GameBoard(
            game_type = game_type,
            animal_type = animal_type,
            gender = gender,
            answer = [card.id for card in answer_cards],
            animals = [card.id for card in group]
            )
        game_boards.append(game_board)

    return game_boards
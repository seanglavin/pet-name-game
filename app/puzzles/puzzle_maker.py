import re
from typing import List
from app.database.models import AnimalCard
from app.database.crud import get_animal_cards


async def apply_name_filter(animal_cards: AnimalCard) -> List[AnimalCard]:
    filtered_cards = []

    name_filter_regex = re.compile('^[a-zA-Z ]+$')
    exclude_words_regex = re.compile('(adopt|adoption|adopted|foster|courtesy|needs|needed|friend|partner|bonded)')

    for card in animal_cards:
        if name_filter_regex.match(card.name) and not exclude_words_regex.search(card.name):
            filtered_cards.append(card)      

    return filtered_cards
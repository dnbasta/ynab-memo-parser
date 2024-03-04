from dataclasses import dataclass
from typing import Literal

from ynabmemoparser.models.category import Category


@dataclass
class SubTransaction:
	payee_name: str
	category: Category
	amount: int
	flag_color: Literal['red', 'green', 'blue', 'orange', 'purple', 'yellow']

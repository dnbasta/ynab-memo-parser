from dataclasses import dataclass

from ynabmemoparser.models.category import Category
from ynabmemoparser.models.payee import Payee


@dataclass(frozen=True)
class OriginalSubTransaction:
	payee: Payee
	category: Category
	memo: str
	amount: int

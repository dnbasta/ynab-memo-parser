from dataclasses import dataclass

from ynabmemoparser.models import Category
from ynabmemoparser.models import Payee


@dataclass(frozen=True)
class OriginalSubTransaction:
	"""Represents an YNAB Subtransaction as part of an existing split transaction

	:ivar payee: The payee of the subtransaction
	:ivar category: The category of the subtransaction
	:ivar amount: The amount of the subtransaction in milliunits
	:ivar memo: The memo of the subtransaction
	"""
	payee: Payee
	category: Category
	memo: str
	amount: int

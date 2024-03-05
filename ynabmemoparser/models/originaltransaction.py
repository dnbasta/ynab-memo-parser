from dataclasses import dataclass
from datetime import date, datetime
from typing import Literal, List, FrozenSet

from ynabmemoparser.models.category import Category
from ynabmemoparser.models.payee import Payee
from ynabmemoparser.models.subtransaction import SubTransaction


@dataclass(frozen=True)
class OriginalTransaction:
	id: str
	transaction_date: date
	category: Category
	amount: int
	memo: str
	payee: Payee
	flag_color: Literal['red', 'green', 'blue', 'orange', 'purple', 'yellow']
	original_memo: str
	original_payee: str
	subtransactions: FrozenSet[SubTransaction]

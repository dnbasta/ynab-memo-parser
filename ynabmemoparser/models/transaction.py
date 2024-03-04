from dataclasses import dataclass
from datetime import date
from typing import Literal, List

from ynabmemoparser.models.category import Category
from ynabmemoparser.models.payee import Payee
from ynabmemoparser.models.subtransaction import SubTransaction


@dataclass
class Transaction:
	id: str
	transaction_date: date
	category: Category
	memo: str
	payee: Payee
	flag_color: Literal['red', 'green', 'blue', 'orange', 'purple', 'yellow']
	original_memo: str
	original_payee: str
	subtransactions: List[SubTransaction]


class ParsedTransaction(Transaction):
	_original: Transaction

	def changed(self) -> bool:
		if self == self._original:
			return False
		return True

	def as_dict(self):
		return dict(id=self.id, memo=self.memo, payee_name=self.payee.name)

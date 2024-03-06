from dataclasses import dataclass

from ynabmemoparser.models.category import Category
from ynabmemoparser.models.payee import Payee


@dataclass
class ParsedSubTransaction:
	payee: Payee
	category: Category
	memo: str
	amount: int

	def as_dict(self) -> dict:
		return dict(payee_id=self.payee.id,
					category_id=self.category.id,
					amount=self.amount,
					memo=self.memo)

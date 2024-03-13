from dataclasses import dataclass

from ynabmemoparser.models import Category
from ynabmemoparser.models import Payee


@dataclass
class SubTransaction:
	"""YNAB Subtransaction object for creating split transactions. To be used as element in subtransaction attribute of
	Transaction class

	:ivar category: The category of the subtransaction
	:ivar payee: The payee of the subtransaction
	:ivar amount: The amount of the subtransaction in milliunits
	:ivar memo: The memo of the subtransaction
	"""
	payee: Payee
	category: Category
	memo: str
	amount: int

	def as_dict(self) -> dict:
		return dict(payee_id=self.payee.id,
					category_id=self.category.id,
					amount=self.amount,
					memo=self.memo)

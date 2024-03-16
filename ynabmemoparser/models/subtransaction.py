from typing import Optional

from pydantic import BaseModel, model_validator

from ynabmemoparser.models.category import Category
from ynabmemoparser.models.payee import Payee


class SubTransaction(BaseModel):
	"""YNAB Subtransaction object for creating split transactions. To be used as element in subtransaction attribute of
	Transaction class

	:ivar category: The category of the subtransaction
	:ivar payee: The payee of the subtransaction
	:ivar amount: The amount of the subtransaction in milliunits
	:ivar memo: The memo of the subtransaction
	"""
	payee: Payee
	category: Category
	memo: Optional[str]
	amount: int

	def as_dict(self) -> dict:
		return dict(payee_id=self.payee.id,
					category_id=self.category.id,
					amount=self.amount,
					memo=self.memo)

	@model_validator(mode='after')
	def check_values(self):
		if self.amount == 0:
			raise ValueError('Amount needs to be different from 0')
		return self

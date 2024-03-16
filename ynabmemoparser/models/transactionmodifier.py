from pydantic import BaseModel, model_validator
from datetime import date
from typing import List, Literal, Optional

from ynabmemoparser.models.category import Category
from ynabmemoparser.models.originaltransaction import OriginalTransaction
from ynabmemoparser.models.subtransaction import SubTransaction
from ynabmemoparser.models.payee import Payee


class TransactionModifier(BaseModel):
	"""Transaction object prefilled with values from original transaction which can take modified values

	:ivar category: The category of the transaction
	:ivar transaction_date: The date of the transaction
	:ivar memo: The memo of the transaction
	:ivar payee: The payee of the transaction
	:ivar flag_color: The flag color of the transaction
	:ivar subtransactions: The subtransactions of the transaction
	"""

	transaction_date: date
	category: Category
	memo: Optional[str]
	payee: Payee
	flag_color: Optional[Literal['red', 'green', 'blue', 'orange', 'purple', 'yellow']]
	subtransactions: List[SubTransaction]

	@classmethod
	def from_original_transaction(cls, original_transaction: OriginalTransaction):
		return cls(transaction_date=original_transaction.transaction_date,
				   category=original_transaction.category,
				   payee=original_transaction.payee,
				   memo=original_transaction.memo,
				   flag_color=original_transaction.flag_color,
				   subtransactions=[])

	@model_validator(mode='after')
	def check_values(self):
		if len(self.subtransactions) == 1:
			raise ValueError(f"There must be at least two subtransactions for a split")
		return self

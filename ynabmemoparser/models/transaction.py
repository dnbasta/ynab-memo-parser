from dataclasses import dataclass
from datetime import date, datetime
from typing import List, Literal, Union

from ynabmemoparser.exceptions import ExistingSubTransactionError
from ynabmemoparser.models.category import Category
from ynabmemoparser.models.originaltransaction import OriginalTransaction
from ynabmemoparser.models.subtransaction import SubTransaction
from ynabmemoparser.models.payee import Payee


@dataclass
class Transaction:
	original: OriginalTransaction
	transaction_date: date
	category: Category
	memo: str
	payee: Payee
	flag_color: Union[Literal['red', 'green', 'blue', 'orange', 'purple', 'yellow'], None]
	subtransactions: List[SubTransaction]

	@classmethod
	def from_original_transaction(cls, original_transaction: OriginalTransaction):
		return cls(original=original_transaction,
				   transaction_date=original_transaction.transaction_date,
				   category=original_transaction.category,
				   payee=original_transaction.payee,
				   memo=original_transaction.memo,
				   flag_color=original_transaction.flag_color,
				   subtransactions=[])

	def changed(self) -> bool:
		if (self.payee != self.original.payee
				or self.transaction_date != self.original.transaction_date
				or self.category != self.original.category
				or self.memo != self.original.memo
				or self.flag_color != self.original.flag_color):
			return True

		if len(self.subtransactions) > 0:
			if len(self.original.subtransactions) > 0:
				raise ExistingSubTransactionError(f"Existing Subtransactions can not be updated", self)
			return True
		return False

	def as_dict(self) -> dict:
		t_dict = dict(id=self.original.id,
					memo=self.memo,
					payee_name=self.payee.name,
					payee_id=self.payee.id,
					category_id=self.category.id,
					flag_color=self.flag_color,
					date=datetime.strftime(self.transaction_date, '%Y-%m-%d'))
		if len(self.subtransactions) > 0 & len(self.original.subtransactions) == 0:
			t_dict = {**t_dict, 'subtransactions': [s.as_dict() for s in self.subtransactions]}
		return t_dict

import dataclasses
from dataclasses import dataclass
from datetime import datetime

from ynabmemoparser.exceptions import ExistingSubTransactionError
from ynabmemoparser.models.originaltransaction import OriginalTransaction
from ynabmemoparser.models.transactionmodifier import TransactionModifier


@dataclass
class ModifiedTransaction:
	original_transaction: OriginalTransaction
	transaction_modifier: TransactionModifier

	def is_changed(self) -> bool:
		"""Helper function to determine if transaction has been altered as compared to original one

		:returns: True if values from original transaction have been altered, False otherwise
		"""
		if (self.transaction_modifier.payee != self.original_transaction.payee
				or self.transaction_modifier.transaction_date != self.original_transaction.transaction_date
				or self.transaction_modifier.category != self.original_transaction.category
				or self.transaction_modifier.memo != self.original_transaction.memo
				or self.transaction_modifier.flag_color != self.original_transaction.flag_color
				or len(self.transaction_modifier.subtransactions) > 0):
			return True
		return False

	def as_dict(self) -> dict:
		"""Returns a dictionary representation of the transaction"""
		t_dict = dict(id=self.original_transaction.id,
					memo=self.transaction_modifier.memo,
					payee_name=self.transaction_modifier.payee.name,
					payee_id=self.transaction_modifier.payee.id,
					category_id=self.transaction_modifier.category.id,
					flag_color=self.transaction_modifier.flag_color,
					date=datetime.strftime(self.transaction_modifier.transaction_date, '%Y-%m-%d'))
		if len(self.transaction_modifier.subtransactions) > 0:
			t_dict = {**t_dict, 'subtransactions': [s.as_dict() for s in self.transaction_modifier.subtransactions]}
		return t_dict

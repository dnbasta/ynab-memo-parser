from dataclasses import dataclass
from datetime import datetime

from ynabmemoparser.exceptions import ExistingSubTransactionError
from ynabmemoparser.models.originaltransaction import OriginalTransaction
from ynabmemoparser.models.transactionmodifier import TransactionModifier

@dataclass
class ModifiedTransaction:
	original_transaction: OriginalTransaction
	transaction_modifier: TransactionModifier

	def raise_on_invalid(self):
		"""Raise an exception if the modifier attempts changes which are not possible

		:raises ExistingSubTransactionError: if modifier contains subtransaction for existing split transactions as
		YNAB API doesn't allow changes to existing subtransactions
		"""

		if len(self.transaction_modifier.subtransactions) > 0:
			if len(self.original_transaction.subtransactions) > 0:
				raise ExistingSubTransactionError(f"Existing Subtransactions can not be updated", self)

	def is_changed(self) -> bool:
		"""Helper function to determine if transaction has been altered as compared to original one

		:returns: True if values from original transaction have been altered, False otherwise
		"""
		if (self.transaction_modifier.payee != self.original_transaction.payee
				or self.transaction_modifier.transaction_date != self.original_transaction.transaction_date
				or self.transaction_modifier.category != self.original_transaction.category
				or self.transaction_modifier.memo != self.original_transaction.memo
				or self.transaction_modifier.flag_color != self.original_transaction.flag_color)\
				or len(self.transaction_modifier.subtransactions) > 0:
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

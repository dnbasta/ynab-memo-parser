from dataclasses import dataclass

from ynabmemoparser.exceptions import ExistingSubTransactionError
from ynabmemoparser.models import TransactionModifier, OriginalTransaction


@dataclass
class ModifiedTransaction:
	original_transaction: OriginalTransaction
	transaction_modifier: TransactionModifier

	def changed(self) -> bool:
		"""Helper function to determine if transaction has been altered as compared to original one

		:returns: True if values from original transaction have been altered, False otherwise
		"""
		if (self.transaction_modifier.payee != self.original_transaction.payee
				or self.transaction_modifier.transaction_date != self.original_transaction.transaction_date
				or self.transaction_modifier.category != self.original_transaction.category
				or self.transaction_modifier.memo != self.original_transaction.memo
				or self.transaction_modifier.flag_color != self.original_transaction.flag_color):
			return True

		if len(self.transaction_modifier.subtransactions) > 0:
			if len(self.original_transaction.subtransactions) > 0:
				raise ExistingSubTransactionError(f"Existing Subtransactions can not be updated", self)
			return True
		return False

	def as_dict(self) -> dict:
		"""Returns a dictionary representation of the transaction"""
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

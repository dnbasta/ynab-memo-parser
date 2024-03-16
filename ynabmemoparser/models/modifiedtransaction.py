from datetime import datetime

from pydantic import BaseModel, model_validator

from ynabmemoparser.models.originaltransaction import OriginalTransaction
from ynabmemoparser.models.transactionmodifier import TransactionModifier


class ModifiedTransaction(BaseModel):
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

	@model_validator(mode='after')
	def check_values(self):
		if len(self.transaction_modifier.subtransactions) > 1:
			if len(self.original_transaction.subtransactions) > 1:
				raise ValueError(f"Existing Subtransactions can not be updated")
			if sum(a.amount for a in self.transaction_modifier.subtransactions) != self.original_transaction.amount:
				raise ValueError('Amount of subtransactions needs to be equal to amount of original transaction')
		return self

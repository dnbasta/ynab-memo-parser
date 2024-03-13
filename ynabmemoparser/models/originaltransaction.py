from dataclasses import dataclass, asdict
from datetime import date, datetime
from typing import Literal, FrozenSet

from ynabmemoparser.models.category import Category
from ynabmemoparser.models.payee import Payee
from ynabmemoparser.models.originalsubtransaction import OriginalSubTransaction


@dataclass(frozen=True)
class OriginalTransaction:
	"""Represents original transaction from YNAB

	:ivar id: The original transaction id
	:ivar amount: The transaction amount in milliunits format
	:ivar category: The category of the original transaction
	:ivar transaction_date: The date of the original transaction
	:ivar memo: The memo of the original transaction
	:ivar payee: The payee of the original transaction
	:ivar flag_color: The flag color of the original transaction
	:ivar import_payee_name: The payee as recorded by YNAB on import
	:ivar import_payee_name_original: The original payee or memo as recorded by the bank
	"""
	id: str
	transaction_date: date
	category: Category
	amount: int
	memo: str
	payee: Payee
	flag_color: Literal['red', 'green', 'blue', 'orange', 'purple', 'yellow']
	import_payee_name_original: str
	import_payee_name: str
	subtransactions: FrozenSet[OriginalSubTransaction]

	@classmethod
	def from_dict(cls, t_dict: dict) -> 'OriginalTransaction':
		def build_subtransaction(s_dict: dict) -> OriginalSubTransaction:
			st_category = Category(id=s_dict['category_id'], name=s_dict['category_name'])
			st_payee = Payee(id=s_dict['payee_id'], name=s_dict['payee_name'], transfer_account_id=s_dict['transfer_account_id'])
			return OriginalSubTransaction(payee=st_payee,
										  category=st_category,
										  amount=s_dict['amount'],
										  memo=s_dict['memo'])

		category = Category(id=t_dict['category_id'], name=t_dict['category_name'])
		payee = Payee(id=t_dict['payee_id'], name=t_dict['payee_name'], transfer_account_id=t_dict['transfer_account_id'])
		return OriginalTransaction(id=t_dict['id'],
								   transaction_date=datetime.strptime(t_dict['date'], '%Y-%m-%d'),
								   category=category,
								   memo=t_dict['memo'],
								   import_payee_name_original=t_dict['import_payee_name_original'],
								   import_payee_name=t_dict['import_payee_name'],
								   flag_color=t_dict['flag_color'],
								   payee=payee,
								   subtransactions=frozenset([build_subtransaction(st) for st in t_dict['subtransactions']]),
								   amount=t_dict['amount'])

	def as_dict(self) -> dict:
		return asdict(self)

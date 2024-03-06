from dataclasses import dataclass
from datetime import date, datetime
from typing import Literal, FrozenSet

from ynabmemoparser.models.category import Category
from ynabmemoparser.models.payee import Payee
from ynabmemoparser.models.originalsubtransaction import OriginalSubTransaction


@dataclass(frozen=True)
class OriginalTransaction:
	id: str
	transaction_date: date
	category: Category
	amount: int
	memo: str
	payee: Payee
	flag_color: Literal['red', 'green', 'blue', 'orange', 'purple', 'yellow']
	original_memo: str
	original_payee: str
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
								   original_memo=t_dict['import_payee_name_original'],
								   original_payee=t_dict['import_payee_name'],
								   flag_color=t_dict['flag_color'],
								   payee=payee,
								   subtransactions=frozenset([build_subtransaction(st) for st in t_dict['subtransactions']]),
								   amount=t_dict['amount'])

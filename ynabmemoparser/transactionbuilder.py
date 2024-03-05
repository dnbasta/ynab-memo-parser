from datetime import datetime

from ynabmemoparser.models.subtransaction import SubTransaction
from ynabmemoparser.models.originaltransaction import OriginalTransaction
from ynabmemoparser.models.transaction import Transaction
from ynabmemoparser.repos.categoryrepo import CategoryRepo
from ynabmemoparser.repos.payeerepo import PayeeRepo


class TransactionBuilder:

	def __init__(self, category_repo: CategoryRepo, payee_repo: PayeeRepo):
		self._payee_repo = payee_repo
		self._category_repo = category_repo

	def build(self, t_dict: dict) -> Transaction:
		original = self.build_original(t_dict)
		return Transaction.from_original_transaction(original)

	def build_original(self, t_dict: dict) -> OriginalTransaction:
		return OriginalTransaction(id=t_dict['id'],
								   transaction_date=datetime.strptime(t_dict['transaction_date'], '%Y-%m-%d'),
								   category=self._category_repo.fetch_by_id(t_dict['category_id']),
								   memo=t_dict['memo'],
								   original_memo=t_dict['import_payee_name_original'],
								   original_payee=t_dict['import_payee_name'],
								   flag_color=t_dict['flag_color'],
								   payee=self._payee_repo.fetch_payee_by_id(t_dict['payee_id']),
								   subtransactions=frozenset([self._build_subtransaction(st) for st in t_dict['subtransactions']]),
								   amount=t_dict['amount'])

	def _build_subtransaction(self, s_dict: dict) -> SubTransaction:
		return SubTransaction(payee=self._payee_repo.fetch_payee_by_id(s_dict['payee_id']),
							  category=self._category_repo.fetch_by_id(s_dict['category_id']),
							  amount=s_dict['amount'],
							  memo=s_dict['memo'])



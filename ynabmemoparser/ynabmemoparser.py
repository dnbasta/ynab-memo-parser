from typing import List, Type

from ynabmemoparser.client import Client
from ynabmemoparser.models import OriginalTransaction, ModifiedTransaction
from ynabmemoparser.parser import Parser
from ynabmemoparser.models import TransactionModifier
from ynabmemoparser.repos import CategoryRepo
from ynabmemoparser.repos import PayeeRepo

YNAB_BASE_URL = 'https://api.youneedabudget.com/v1'


class YnabMemoParser:
	"""The primary class object of the library. It takes all configuration input and contains functions to fetch,
	parse and update transactions

	:param budget: The YNAB budget id to use
	:param account: The YNAB account id to use
	:param token: The YNAB token to use

	:ivar categories: Lookup of categories associated with the budget
	:ivar payees: Lookup of payees associated with the budget
	"""

	def __init__(self, budget: str, account: str, token: str) -> None:
		self._budget = budget
		self._account = account
		self._client = Client(token=token, budget=budget, account=account)
		self.categories: CategoryRepo = CategoryRepo(self._client.fetch_categories())
		self.payees: PayeeRepo = PayeeRepo(self._client.fetch_payees())

	def fetch_transactions(self) -> List[OriginalTransaction]:
		"""
		Fetches all transactions from YNAB account
		:returns: list of original YNAB transactions
		"""
		return self._client.fetch_transactions()

	def parse_transactions(self, transactions: List[OriginalTransaction],
						   parser_class: Type[Parser]) -> List[ModifiedTransaction]:
		"""Parses original transactions with provided parser class. The method checks for allowed changes
		and returns a list of the modified transactions

		:param transactions: list of original transactions from YNAB
		:param parser_class: The Parser child class to use
		:return: list of modified transactions

		:raises ExistingSubTransactionError: if original transaction and transaction modifier contain subtransactions
		since the YNAB API doesn't allow modifying existing split transactions
		"""
		parser = parser_class(categories=self.categories, payees=self.payees)
		transaction_tuples = [(t, TransactionModifier.from_original_transaction(t)) for t in transactions]
		parsed_transaction_tuples = [(t[0], parser.parse(original=t[0],
															   modifier=t[1])) for t in transaction_tuples]
		modified_transactions = [ModifiedTransaction(original_transaction=t[0],
													 transaction_modifier=t[1]) for t in parsed_transaction_tuples]

		[t.raise_on_invalid() for t in modified_transactions]
		return modified_transactions

	@staticmethod
	def _check_change_exceptions(mt: ModifiedTransaction) -> ModifiedTransaction:
		try:
			mt.changed()
			return mt
		except Exception as e:
			raise e

	def update_transactions(self, transactions: List[ModifiedTransaction]) -> int:
		"""Filters list of modified transactions for actual changes and updates the respective transactions in YNAB

		:param transactions: List of modified transactions to update in YNAB
		:returns: number of updated transactions
		"""
		filtered_transactions = [t for t in transactions if t.is_changed()]
		return self._client.update_transactions(filtered_transactions)


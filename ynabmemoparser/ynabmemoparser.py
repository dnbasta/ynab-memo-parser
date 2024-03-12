from typing import List, Type

from ynabmemoparser.client import Client
from ynabmemoparser.models import OriginalTransaction
from ynabmemoparser.parser import Parser
from ynabmemoparser.models.transaction import Transaction
from ynabmemoparser.repos.categoryrepo import CategoryRepo
from ynabmemoparser.repos.payeerepo import PayeeRepo

YNAB_BASE_URL = 'https://api.youneedabudget.com/v1'


class YnabMemoParser:
	"""The primary class object of the library. It takes all configuration input and contains functions to fetch,
	parse and update transactions

	:param budget: The YNAB budget id to use
	:param account: The YNAB account id to use
	:param token: The YNAB token to use
	:param parser_class: The Parser child class to use
	"""

	def __init__(self, budget: str, account: str, token: str, parser_class: Type[Parser]) -> None:
		self._budget = budget
		self._account = account
		self._client = Client(token=token, budget=budget, account=account)
		self.parser = parser_class(categories=CategoryRepo(self._client), payees=PayeeRepo(self._client))

	def fetch_transactions(self) -> List[OriginalTransaction]:
		"""
		Fetches all transactions from YNAB account
		:returns: list of original YNAB transactions
		"""
		return self._client.fetch_transactions()

	def parse_transactions(self, transactions: List[OriginalTransaction]) -> List[Transaction]:
		"""Parses original transactions and returns modified transactions

		:param transactions: list of original transactions from YNAB
		:return: list of modified YNAB transactions
		"""
		transactions = [Transaction.from_original_transaction(t) for t in transactions]
		parsed_transactions = [self.parser.parse(t) for t in transactions]
		filtered_parsed_transactions = [t for t in parsed_transactions if t.changed()]
		return filtered_parsed_transactions

	def update_transactions(self, transactions: List[Transaction]) -> int:
		"""Updates the transactions in YNAB

		:param transactions: List of modified transactions to update in YNAB
		:returns: number of updated transactions
		"""
		return self._client.update_transactions(transactions)


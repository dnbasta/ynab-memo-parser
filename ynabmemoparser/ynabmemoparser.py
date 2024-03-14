import logging
from typing import List, Type

from ynabmemoparser.client import Client
from ynabmemoparser.exceptions import ParserError
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

		:raises ParserError: if there is an error while executing parser
		:raises ExistingSubTransactionError: if original transaction and transaction modifier contain subtransactions
		since the YNAB API doesn't allow modifying existing split transactions
		"""
		parser = parser_class(categories=self.categories, payees=self.payees)
		modified_transactions = [self._parse_transaction(original=t, parser=parser) for t in transactions]
		successfully_parsed = [mt for mt in modified_transactions if mt is not None]
		return successfully_parsed

	@staticmethod
	def _parse_transaction(original: OriginalTransaction, parser: Parser) -> ModifiedTransaction:
		modifier = TransactionModifier.from_original_transaction(original_transaction=original)
		try:
			modifier_return = parser.parse(original=original, modifier=modifier)
			if not isinstance(modifier_return, TransactionModifier):
				raise ParserError(f"Parser {parser.__class__.__name__} doesn't return TransactionModifier object")
			modified_transaction = ModifiedTransaction(original_transaction=original,
													 transaction_modifier=modifier_return)
			modified_transaction.raise_on_invalid()
			return modified_transaction
		except Exception as e:
			raise ParserError(f"Error while parsing {original.as_dict()} with {parser.__class__.__name__}")

	def update_transactions(self, transactions: List[ModifiedTransaction]) -> int:
		"""Filters list of modified transactions for actual changes and updates the respective transactions in YNAB

		:param transactions: List of modified transactions to update in YNAB
		:returns: number of updated transactions
		"""
		filtered_transactions = [t for t in transactions if t.is_changed()]
		return self._client.update_transactions(filtered_transactions)

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
						   parser_class: Type[Parser],
						   return_only_changed: bool = True) -> List[ModifiedTransaction]:
		"""Parses original transactions with provided parser class. The method checks for allowed changes
		and returns a list of the modified transactions

		:param transactions: list of original transactions from YNAB
		:param parser_class: The Parser child class to use
		:param return_only_changed: If set to False returns all transactions no matter whether they were changed or not
		:return: list of modified transactions

		:raises ParserError: if there is an error in parsing a transaction either during the parsing itself or upon
		validating the result
		"""
		parser = parser_class(categories=self.categories, payees=self.payees)
		modified_transactions = [self._parse_transaction(original=t, parser=parser) for t in transactions]
		if return_only_changed:
			modified_transactions = [t for t in modified_transactions if t.is_changed()]
		return modified_transactions

	def _parse_transaction(self, original: OriginalTransaction, parser: Parser) -> ModifiedTransaction:
		modifier = TransactionModifier.from_original_transaction(original_transaction=original)
		try:
			modifier_return = parser.parse(original=original, modifier=modifier)
			if not isinstance(modifier_return, TransactionModifier):
				raise ParserError(f"Parser {parser.__class__.__name__} doesn't return TransactionModifier object")
			TransactionModifier.model_validate(modifier_return.__dict__)
			self.categories.fetch_by_id(modifier_return.category.id)
			modified_transaction = ModifiedTransaction(original_transaction=original,
													 transaction_modifier=modifier_return)
			return modified_transaction
		except Exception as e:
			raise ParserError(f"Error while parsing {original.as_dict()} with {parser.__class__.__name__}") from e

	def update_transactions(self, transactions: List[ModifiedTransaction]) -> int:
		"""Takes a list of modified transactions and updates the respective transactions in YNAB

		:param transactions: List of modified transactions to update in YNAB
		:returns: number of updated transactions
		"""
		return self._client.update_transactions(transactions)

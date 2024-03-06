from dataclasses import dataclass
from typing import List, Type

from ynabmemoparser.client import Client
from ynabmemoparser.models.originaltransaction import OriginalTransaction
from ynabmemoparser.parser import Parser
from ynabmemoparser.models.transaction import Transaction
from ynabmemoparser.repos.categoryrepo import CategoryRepo
from ynabmemoparser.repos.payeerepo import PayeeRepo

YNAB_BASE_URL = 'https://api.youneedabudget.com/v1'


@dataclass
class YnabMemoParser:

	def __init__(self, budget: str, account: str, token: str, parser_class: Type[Parser]) -> None:
		self._budget = budget
		self._account = account
		self._client = Client(token=token, budget=budget, account=account)
		self.parser = parser_class(categories=CategoryRepo(self._client), payees=PayeeRepo(self._client))

	def fetch_transactions(self) -> List[OriginalTransaction]:
		return self._client.fetch_transactions()

	def parse_transactions(self, transactions: List[OriginalTransaction]) -> List[Transaction]:
		transactions = [Transaction.from_original_transaction(t) for t in transactions]
		parsed_transactions = [self.parser.parse(t) for t in transactions]
		filtered_parsed_transactions = [t for t in parsed_transactions if t.changed()]
		return filtered_parsed_transactions

	def update_transactions(self, transactions: List[Transaction]) -> int:
		return self._client.update_transactions(transactions)

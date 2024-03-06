from dataclasses import dataclass
from typing import List, Type

from ynabmemoparser.client import Client
from ynabmemoparser.models.transaction import Transaction
from ynabmemoparser.parser import Parser
from ynabmemoparser.models.parsedtransaction import ParsedTransaction
from ynabmemoparser.repos.categoryrepo import CategoryRepo
from ynabmemoparser.repos.payeerepo import PayeeRepo

YNAB_BASE_URL = 'https://api.youneedabudget.com/v1'


@dataclass
class YnabMemoParser:

	def __init__(self, budget: str, account: str, token: str, parser_class: Type[Parser]) -> None:
		self._budget = budget
		self._account = account
		self._client = Client(token=token, budget=budget, account=account)
		self.category_repo = CategoryRepo(self._client)
		self.payee_repo = PayeeRepo(self._client)
		self.parser = parser_class(category_repo=self.category_repo, payee_repo=self.payee_repo)

	def fetch_transactions(self) -> List[Transaction]:
		return self._client.fetch_transactions()

	def parse_transactions(self, transactions: List[Transaction]) -> List[ParsedTransaction]:
		transactions = [ParsedTransaction.from_original_transaction(t) for t in transactions]
		parsed_transactions = [self.parser.parse(t) for t in transactions]
		filtered_parsed_transactions = [t for t in parsed_transactions if t.changed()]
		return filtered_parsed_transactions

	def update_transactions(self, transactions: List[ParsedTransaction]) -> int:
		return self._client.update_transactions(transactions)

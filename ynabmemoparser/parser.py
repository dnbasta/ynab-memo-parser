from abc import abstractmethod

from ynabmemoparser.models.parsedtransaction import ParsedTransaction
from ynabmemoparser.repos.categoryrepo import CategoryRepo
from ynabmemoparser.repos.payeerepo import PayeeRepo


class Parser:

	def __init__(self, category_repo: CategoryRepo, payee_repo=PayeeRepo):
		self.category_repo = category_repo
		self.payee_repo = payee_repo

	@abstractmethod
	def parse(self, transaction: ParsedTransaction) -> ParsedTransaction:
		pass

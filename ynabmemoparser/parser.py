from abc import abstractmethod

from ynabmemoparser.models.transaction import Transaction
from ynabmemoparser.repos.categoryrepo import CategoryRepo
from ynabmemoparser.repos.payeerepo import PayeeRepo


class Parser:

	def __init__(self, categories: CategoryRepo, payees=PayeeRepo):
		self.categories = categories
		self.payees = payees

	@abstractmethod
	def parse(self, transaction: Transaction) -> Transaction:
		pass

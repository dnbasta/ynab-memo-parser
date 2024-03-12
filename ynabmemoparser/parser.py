from abc import abstractmethod

from ynabmemoparser.models.transaction import Transaction
from ynabmemoparser.repos.categoryrepo import CategoryRepo
from ynabmemoparser.repos.payeerepo import PayeeRepo


class Parser:
	"""Abstract class which modifies transactions according to concrete implementation. You need to create your own
	child class and implement the parse method in it according to your needs. It has attributes which allow you to
	lookup categories and payees from your budget.

	:ivar categories: Collection of current categories in YNAB budget
	:ivar payees: Collection of current payees in YNAB budget
	"""
	def __init__(self, categories: CategoryRepo, payees: PayeeRepo):
		self.categories: CategoryRepo = categories
		self.payees: PayeeRepo = payees

	@abstractmethod
	def parse(self, transaction: Transaction) -> Transaction:
		"""Function which implements the actual modification of a transaction. It is initiated and called by the library
		for all transactions provided in the parse_transaction method of the main class.

		:param transaction: Transaction to be modified prefilled with values from original transaction
		:returns: Has to return the modified transaction
		"""
		pass

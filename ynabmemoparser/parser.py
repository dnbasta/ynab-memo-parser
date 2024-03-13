from abc import abstractmethod

from ynabmemoparser.models import TransactionModifier, OriginalTransaction
from ynabmemoparser.repos import CategoryRepo
from ynabmemoparser.repos import PayeeRepo


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
	def parse(self, original: OriginalTransaction, modifier: TransactionModifier) -> TransactionModifier:
		"""Function which implements the actual modification of a transaction. It is initiated and called by the library
		for all transactions provided in the parse_transaction method of the main class.

		:param original: Original transaction
		:param modifier: Transaction modifier prefilled with values from original transaction. All attributes can be
		changed and will modify the transaction
		:returns: Method needs to return the transaction modifier after modification
		"""
		pass

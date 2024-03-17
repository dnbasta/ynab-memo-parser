
class NoMatchingCategoryError(Exception):
	"""Raised when no matching category is found in the specified budget"""
	pass


class MultipleMatchingCategoriesError(Exception):
	"""Raised when multiple matching categories are found in the specified budget. This can be the case when categories
	have the same name under different category groups"""
	pass


class NoMatchingPayeeError(Exception):
	"""Raised when no matching payee is found in the specified budget"""
	pass


class ExistingSubTransactionError(Exception):
	"""Raised when subtransactions are specified in the modifier for a transaction which already has subtransactions.
	YNAB currently doesn't allow updating splits of existing split transactions via the API"""
	pass


class ParserError(Exception):
	pass

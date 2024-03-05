
class NoMatchingCategoryError(Exception):
	pass


class MultipleMatchingCategoriesError(Exception):
	pass


class NoMatchingPayeeError(Exception):
	pass


class ExistingSubTransactionError(Exception):
	pass

from ynabmemoparser.client import Client
from ynabmemoparser.exceptions import NoMatchingCategoryError, MultipleMatchingCategoriesError
from ynabmemoparser.models.category import Category


class CategoryRepo:

	def __init__(self, client: Client):
		self._categories = client.fetch_categories()

	def fetch_by_name(self, category_name: str, group_name: str = None) -> Category:
		cats = [c for cg in self._categories for c in cg.categories if category_name == c.name]

		if group_name:
			cats = [c for c in cats if c.name == group_name]

		if len(cats) == 1:
			return cats[0]
		elif len(cats) > 1:
			raise MultipleMatchingCategoriesError(category_name, cats)
		raise NoMatchingCategoryError(category_name)

	def fetch_by_id(self, category_id: str) -> Category:
		try:
			return next(c for cg in self._categories for c in cg.categories if c.id == category_id)
		except StopIteration:
			raise NoMatchingCategoryError(category_id)

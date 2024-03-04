from ynabmemoparser.client import Client
from ynabmemoparser.exceptions import NoMatchingCategoryError, MultipleMatchingCategoriesError
from ynabmemoparser.models.category import Category


class CategoryRepo:

	def __init__(self, client: Client):
		self.category_groups = client.fetch_categories()

	def fetch_by_name(self, category_name: str, group_name: str = None) -> Category:
		cats = [cg for cg in self.category_groups if category_name in [c.name for c in cg.categories]]

		if group_name:
			cats = [cg for cg in cats if cg.name == group_name]

		if len(cats) == 1:
			return next(c for c in cats[0].categories if c.name == category_name)
		elif len(cats) > 1:
			raise MultipleMatchingCategoriesError(category_name, cats)
		raise NoMatchingCategoryError(category_name)

	def fetch_by_id(self, category_id: str) -> Category:
		try:
			return next(c for cg in self.category_groups for c in cg.categories if c.id == category_id)
		except StopIteration:
			raise NoMatchingCategoryError(category_id)

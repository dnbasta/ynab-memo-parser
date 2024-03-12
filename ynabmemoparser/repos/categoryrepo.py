from typing import List

from ynabmemoparser.client import Client
from ynabmemoparser.exceptions import NoMatchingCategoryError, MultipleMatchingCategoriesError
from ynabmemoparser.models import CategoryGroup
from ynabmemoparser.models.category import Category


class CategoryRepo:
	"""Repository which holds all categories from your YNAB budget
	"""
	def __init__(self, client: Client):
		self._categories: List[CategoryGroup] = client.fetch_categories()

	def fetch_by_name(self, category_name: str, group_name: str = None) -> Category:
		"""Fetches a YNAB category by its name

		:param category_name: Name of the category to fetch
		:param group_name: Optional name of the group the category belongs to
		:return: Matched category by name
		:raises NoMatchingCategoryError: if no matching category is found
		:raises MultipleMatchingCategoriesError: if multiple matching categories are found
		"""
		cats = [c for cg in self._categories for c in cg.categories if category_name == c.name]

		if group_name:
			cats = [c for c in cats if c.name == group_name]

		if len(cats) == 1:
			return cats[0]
		elif len(cats) > 1:
			raise MultipleMatchingCategoriesError(category_name, cats)
		raise NoMatchingCategoryError(category_name)

	def fetch_by_id(self, category_id: str) -> Category:
		"""Fetches a YNAB category by its ID
		:param category_id: ID of the category
		:return: Returns the matched category
		:raises NoMatchingCategoryError: if no matching category is found
		"""
		try:
			return next(c for cg in self._categories for c in cg.categories if c.id == category_id)
		except StopIteration:
			raise NoMatchingCategoryError(category_id)

	def fetch_all_from_group(self, group_name: str) -> List[Category]:
		"""Fetches all categories of a group from YNAB budget

		:param group_name: Name of the group to fetch categories for
		:return: List of all categories in group
		:raises NoMatchingCategoryError: if no matching category is found
		"""
		cat_group = next(c for c in self._categories if c.name == group_name)
		return list(cat_group.categories)

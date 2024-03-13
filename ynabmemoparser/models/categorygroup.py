from dataclasses import dataclass
from typing import FrozenSet

from ynabmemoparser.models.category import Category


@dataclass(frozen=True)
class CategoryGroup:
	"""Represents a YNAB category group in the budget

	:ivar name: The name of the category group
	:ivar categories: The categories in the category group
	"""
	name: str
	categories: FrozenSet[Category]

	@classmethod
	def from_dict(cls, data: dict) -> 'CategoryGroup':
		categories = frozenset([Category(id=c['id'], name=c['name'])
								for c in data['categories'] if c['deleted'] is False])
		return cls(name=data['name'], categories=categories)

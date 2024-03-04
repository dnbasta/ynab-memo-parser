from dataclasses import dataclass
from typing import FrozenSet


@dataclass(frozen=True)
class Category:
	name: str
	id: str


@dataclass(frozen=True)
class CategoryGroup:
	id: str
	name: str
	categories: FrozenSet[Category]

	@classmethod
	def from_dict(cls, g_dict: dict):
		categories = frozenset([Category(id=c['id'], name=c['name']) for c in g_dict['categories'] if c['deleted'] is False])
		return cls(id=g_dict['id'], name=g_dict['name'], categories=categories)


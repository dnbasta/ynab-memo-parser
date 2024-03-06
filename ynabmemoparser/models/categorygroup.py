from dataclasses import dataclass
from typing import FrozenSet

from ynabmemoparser.models.category import Category


@dataclass(frozen=True)
class CategoryGroup:
	name: str
	categories: FrozenSet[Category]

	@classmethod
	def from_dict(cls, data: dict) -> 'CategoryGroup':
		categories = frozenset([Category(id=c['id'], name=c['name'])
								for c in data['categories'] if c['deleted'] is False])
		return cls(name=data['name'], categories=categories)

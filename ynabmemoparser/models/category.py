from dataclasses import dataclass


@dataclass(frozen=True)
class Category:
	"""Category object of YNAB budget

	:ivar id: The ID of the category
	:ivar name: The name of the category
	"""
	id: str
	name: str


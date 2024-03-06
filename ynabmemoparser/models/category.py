from dataclasses import dataclass


@dataclass(frozen=True)
class Category:
	id: str
	name: str


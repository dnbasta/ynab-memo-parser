from dataclasses import dataclass


@dataclass(frozen=True)
class Category:
	name: str
	group_name: str
	id: str


from typing import Optional

from pydantic import BaseModel, ConfigDict


class Category(BaseModel):
	"""Category object of YNAB budget

	:ivar id: The ID of the category
	:ivar name: The name of the category
	"""
	model_config = ConfigDict(frozen=True)
	id: Optional[str]
	name: str


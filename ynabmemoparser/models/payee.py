from typing import Optional

from pydantic import BaseModel, ConfigDict


class Payee(BaseModel):
	"""Represents a YNAB Payee

	:ivar name: The name of the payee
	:ivar id: The ID of the payee
	:ivar transfer_account_id: The ID of the transfer account in case payee is of type "Transfer:[account]"
	"""
	model_config = ConfigDict(frozen=True)
	name: Optional[str]
	id: Optional[str] = None
	transfer_account_id: Optional[str] = None

	@classmethod
	def from_dict(cls, p_dict: dict):
		return cls(name=p_dict['name'], id=p_dict['id'], transfer_account_id=p_dict['transfer_account_id'])


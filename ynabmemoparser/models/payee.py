from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Payee:
	"""Represents a YNAB Payee

	:ivar id: The ID of the payee
	:ivar name: The name of the payee
	:ivar transfer_account_id: The ID of the transfer account in case payee is of type "Transfer:[account]"
	"""
	name: str
	id: Optional[str] = None
	transfer_account_id: Optional[str] = None

	@classmethod
	def from_dict(cls, p_dict: dict):
		return cls(name=p_dict['name'], id=p_dict['id'], transfer_account_id=p_dict['transfer_account_id'])


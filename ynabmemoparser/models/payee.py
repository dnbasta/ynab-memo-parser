from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Payee:
	name: str
	id: str
	transfer_account_id: Optional[str]

	@classmethod
	def from_dict(cls, p_dict: dict):
		return cls(name=p_dict['name'], id=p_dict['id'], transfer_account_id=p_dict['transfer_account_id'])


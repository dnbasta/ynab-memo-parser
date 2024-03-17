from typing import List

from ynabmemoparser.exceptions import NoMatchingPayeeError
from ynabmemoparser.models import Payee


class PayeeRepo:
	"""Repository which holds all payees from your YNAB budget"""

	def __init__(self, payees: List[Payee]):
		self._payees = payees

	def fetch_by_name(self, payee_name: str) -> Payee:
		"""Fetches a payee by its name

		:param payee_name: Name of the payee to fetch
		:return: Matched Payee
		:raises NoMatchingPayeeError: if no matching payee is found
		"""
		try:
			return next(p for p in self._payees if p.name == payee_name)
		except StopIteration:
			raise NoMatchingPayeeError(f"No payee with name '{payee_name}")

	def fetch_by_id(self, payee_id: str) -> Payee:
		"""Fetches a payee by its ID

		:param payee_id: ID of the payee to fetch
		:return: matched payee
		:raises NoMatchingPayeeError: if no matching payee is found
		"""
		try:
			return next(p for p in self._payees if p.id == payee_id)
		except StopIteration:
			raise NoMatchingPayeeError(f"No payee with id '{payee_id}")

	def fetch_by_transfer_account_id(self, transfer_account_id: str) -> Payee:
		"""Fetches a transfer payee by the target account id

		:param transfer_account_id: The id of the target account for the transfer
		:return: matched transfer payee
		:raises NoMatchingPayeeError: if no matching payee is found
		"""
		try:
			return next(p for p in self._payees if p.transfer_account_id == transfer_account_id)
		except StopIteration:
			raise NoMatchingPayeeError(f"No payee found for transfer_account_id {transfer_account_id}")

	def fetch_all(self) -> List[Payee]:
		"""Fetches all payees from YNAB budget

		:return: List of all payees in budget"""
		return self._payees

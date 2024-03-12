from typing import List

from ynabmemoparser.client import Client
from ynabmemoparser.exceptions import NoMatchingPayeeError
from ynabmemoparser.models.payee import Payee


class PayeeRepo:
	"""Repository which holds all payees from your YNAB budget"""

	def __init__(self, client: Client):
		self._payees = client.fetch_payees()

	def fetch_payee_by_name(self, payee_name: str) -> Payee:
		"""Fetches a payee by its name

		:param payee_name: Name of the payee to fetch
		:return: Matched Payee
		:raises NoMatchingPayeeError: if no matching payee is found
		"""
		try:
			return next(p for p in self._payees if p.name == payee_name)
		except StopIteration:
			raise NoMatchingPayeeError(f"No payee with name '{payee_name}")

	def fetch_payee_by_id(self, payee_id: str) -> Payee:
		"""Fetches a payee by its ID

		:param payee_id: ID of the payee to fetch
		:return: matched payee
		:raises NoMatchingPayeeError: if no matching payee is found
		"""
		try:
			return next(p for p in self._payees if p.id == payee_id)
		except StopIteration:
			raise NoMatchingPayeeError(f"No payee with id '{payee_id}")

	def fetch_all(self) -> List[Payee]:
		"""Fetches all payees from YNAB budget

		:return: List of all payees in budget"""
		return self._payees

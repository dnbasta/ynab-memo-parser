from typing import List

from ynabmemoparser.client import Client
from ynabmemoparser.exceptions import NoMatchingPayeeError
from ynabmemoparser.models.payee import Payee


class PayeeRepo:

	def __init__(self, client: Client):
		self._payees = client.fetch_payees()

	def fetch_payee_by_name(self, payee_name: str) -> Payee:
		try:
			return next(p for p in self._payees if p.name == payee_name)
		except StopIteration:
			raise NoMatchingPayeeError(f"No payee with name '{payee_name}")

	def fetch_payee_by_id(self, payee_id: str) -> Payee:
		try:
			return next(p for p in self._payees if p.id == payee_id)
		except StopIteration:
			raise NoMatchingPayeeError(f"No payee with id '{payee_id}")

	def fetch_all(self) -> List[Payee]:
		return self._payees

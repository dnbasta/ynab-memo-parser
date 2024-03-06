from typing import List

import requests

from ynabmemoparser.models.category import Category
from ynabmemoparser.models.categorygroup import CategoryGroup
from ynabmemoparser.models.payee import Payee
from ynabmemoparser.models.transaction import Transaction

YNAB_BASE_URL = 'https://api.ynab.com/v1'


class Client:

	def __init__(self, token: str, budget: str, account: str):
		self._header = {'Authorization': f'Bearer {token}'}
		self._budget = budget
		self._account = account

	def fetch_categories(self) -> List[CategoryGroup]:
		r = requests.get(f'{YNAB_BASE_URL}/budgets/{self._budget}/categories', headers=self._header)
		r.raise_for_status()

		data = r.json()['data']['category_groups']
		categories = [CategoryGroup.from_dict(cg) for cg in data if cg['deleted'] is False]
		return categories

	def fetch_payees(self) -> List[Payee]:
		r = requests.get(f'{YNAB_BASE_URL}/budgets/{self._budget}/payees', headers=self._header)
		r.raise_for_status()

		data = r.json()['data']['payees']
		payees = [Payee.from_dict(p) for p in data if p['deleted'] is False]
		return payees

	def fetch_transaction_dicts(self) -> List[dict]:
		r = requests.get(f'{YNAB_BASE_URL}/budgets/{self._budget}/accounts/{self._account}/transactions', headers=self._header)
		r.raise_for_status()

		data = r.json()['data']['transactions']
		transaction_dicts = [t for t in data if t['deleted'] is False]
		return transaction_dicts

	def update_transactions(self, transactions: List[Transaction]) -> int:
		update_dict = {'transactions': [r.as_dict() for r in transactions]}
		r = requests.patch(f'{YNAB_BASE_URL}/budgets/{self._budget}/transactions',
						   json=update_dict,
						   headers=self._header)
		r.raise_for_status()
		r_dict = r.json()['data']['transaction_ids']
		return len(r_dict)

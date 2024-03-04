from typing import List

import requests

from ynabmemoparser.models.category import CategoryGroup

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
		category_groups = [CategoryGroup.from_dict(cg) for cg in data if cg['deleted'] is False]
		return category_groups

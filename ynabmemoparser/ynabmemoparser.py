from dataclasses import dataclass
from typing import List

import requests

from ynabmemoparser.parser import Parser
from ynabmemoparser.recordbuilder import RecordBuilder
from ynabmemoparser.ynabrecord import YnabRecord

YNAB_BASE_URL = 'https://api.youneedabudget.com/v1'


@dataclass
class YnabMemoParser:

	def __init__(self, budget: str, account: str, token: str) -> None:
		self._budget = budget
		self._account = account
		self._header = {'Authorization': f'Bearer {token}'}

	def fetch_record_dicts(self) -> List[dict]:
		r = requests.get(f'{YNAB_BASE_URL}/budgets/{self._budget}/accounts/{self._account}/transactions',
						 headers=self._header)
		r.raise_for_status()
		transactions_dict = r.json()['data']['transactions']
		return transactions_dict

	@staticmethod
	def parse_records(records_dicts: List[dict], parser: Parser) -> List[YnabRecord]:
		rb = RecordBuilder(parser=parser)
		parsed_records = [rb.build(t) for t in records_dicts]
		return parsed_records

	def update_records(self, ynab_records: List[YnabRecord]) -> int:
		update_dict = {'transactions': [r.as_dict() for r in ynab_records]}
		r = requests.patch(f'{YNAB_BASE_URL}/budgets/{self._budget}/transactions',
						   json=update_dict,
						   headers=self._header)
		r.raise_for_status()
		r_dict = r.json()['data']['transaction_ids']
		return len(r_dict)

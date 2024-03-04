from unittest.mock import MagicMock, patch

from requests import Response

from ynabmemoparser.client import Client
from ynabmemoparser.models.payee import Payee


@patch('ynabmemoparser.client.requests.get')
def test_fetch_categories(get_patch):
	# Arrange
	resp = MagicMock(spec=Response)
	resp.json.return_value = {'data': {'category_groups': [
		{'id': 'cg_id', 'name': 'cg_name', 'deleted': False, 'categories': [{'id': 'c_id', 'name': 'c_name', 'deleted': False},
																			{'id': 'c_id', 'name': 'c_name', 'deleted': True}]},
		{'id': 'cg_id2', 'name': 'cg_name2', 'deleted': True, 'categories': [{'id': 'c_id', 'name': 'c_name', 'deleted': False}]}
	]}}
	get_patch.return_value = resp

	# Act
	c = Client(token=MagicMock(), budget=MagicMock(), account=MagicMock())
	cats = c.fetch_categories()

	# Assert
	assert len(cats) == 1
	assert cats[0].id == 'c_id'
	assert cats[0].name == 'c_name'
	assert cats[0].group_name == 'cg_name'


@patch('ynabmemoparser.client.requests.get')
def test_fetch_payees(mock_get):
	# Arrange
	resp = MagicMock(spec=Response)
	resp.json.return_value = {'data': {'payees': [{
		'id': 'p_id', 'name': 'p_name', 'deleted': False, 'transfer_account_id': 't_id'}]}}
	mock_get.return_value = resp

	# Act
	c = Client(token=MagicMock(), budget=MagicMock(), account=MagicMock())
	p_list = c.fetch_payees()

	# Assert
	assert len(p_list) == 1
	assert isinstance(p_list[0], Payee)
	assert p_list[0].name == 'p_name'
	assert p_list[0].id == 'p_id'
	assert p_list[0].transfer_account_id == 't_id'

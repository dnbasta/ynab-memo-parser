from unittest.mock import MagicMock, patch

from requests import Response

from ynabmemoparser.client import Client


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
	assert cats[0].id == 'cg_id'
	assert cats[0].name == 'cg_name'

	cs = list(cats[0].categories)
	assert len(cs) == 1
	assert cs[0].id == 'c_id'
	assert cs[0].name == 'c_name'

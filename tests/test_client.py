from unittest.mock import MagicMock, patch

from requests import Response

from ynabmemoparser.client import Client


@patch('ynabmemoparser.client.requests.get')
def test_fetch_categories(get_patch):
	resp = MagicMock(spec=Response)
	resp.json.return_value = {'data': {'category_groups': [{'id': 'cg_id', 'name': 'cg_name', 'categories':
						 [{'id': 'c_id', 'name': 'c_name'}]}]}}
	get_patch.return_value = resp
	c = Client(token=MagicMock(), budget=MagicMock(), account=MagicMock())
	cats = c.fetch_categories()
	assert cats[0].id == 'cg_id'
	assert cats[0].name == 'cg_name'
	c = next(iter(cats[0].categories))
	assert c.id == 'c_id'
	assert c.name == 'c_name'

from datetime import date
from unittest.mock import patch

import pytest

from ynabmemoparser import YnabMemoParser
from ynabmemoparser.models import OriginalTransaction, Category, Payee, OriginalSubTransaction, SubTransaction, CategoryGroup
from ynabmemoparser.repos import CategoryRepo


@pytest.fixture
def mock_subtransaction(request):
	return SubTransaction(memo='memo', amount=500,
						  category=Category(name='cname', id=None),
						  payee=Payee(name='pname'))


@pytest.fixture
def mock_original_transaction(request):
	subs = []
	try:
		if request.param:
			ost = OriginalSubTransaction(memo='memo1', amount=500,
								   category=Category(name='cname', id=None),
								   payee=Payee(name='pname'))
			ost2 = OriginalSubTransaction(memo='memo2', amount=500,
								   category=Category(name='cname', id=None),
								   payee=Payee(name='pname'))
			subs = [ost, ost2]
	except AttributeError as e:
		pass
	return OriginalTransaction(id='id',
							   memo='memo',
							   category=Category(id='cid1', name='cname'),
							   payee=Payee(id='pid', name='pname'),
							   subtransactions=frozenset(subs),
							   flag_color='red',
							   amount=1000,
							   import_payee_name='ipn',
							   import_payee_name_original='ipno',
							   transaction_date=date(2024, 1, 1))


@pytest.fixture
def mock_category_repo():
	return CategoryRepo(categories=[
		CategoryGroup(name='group1', categories=frozenset([Category(id='cid1', name='c_name')])),
		CategoryGroup(name='group2', categories=frozenset([Category(id='cid2', name='c_name')]))])


@pytest.fixture
@patch('ynabmemoparser.ynabmemoparser.Client')
def mock_memo_parser(mock_client, mock_category_repo):
	ymp = YnabMemoParser(budget='budget', account='account', token='token')
	ymp.categories = mock_category_repo
	return ymp

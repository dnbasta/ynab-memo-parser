from datetime import date

import pytest

from ynabmemoparser.models import OriginalTransaction, Category, Payee


@pytest.fixture
def mock_original_transaction(request):
	try:
		subs = request.param
	except AttributeError as e:
		subs = []
	return OriginalTransaction(id='id',
							   memo='memo',
							   category=Category(id='cid', name='cname'),
							   payee=Payee(id='pid', name='pname'),
							   subtransactions=frozenset(subs),
							   flag_color='red',
							   amount=1000,
							   import_payee_name='ipn',
							   import_payee_name_original='ipno',
							   transaction_date=date(2024, 1, 1))

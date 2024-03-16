from datetime import date

import pytest

from ynabmemoparser.models import OriginalTransaction, Category, Payee, OriginalSubTransaction, SubTransaction


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
							   category=Category(id='cid', name='cname'),
							   payee=Payee(id='pid', name='pname'),
							   subtransactions=frozenset(subs),
							   flag_color='red',
							   amount=1000,
							   import_payee_name='ipn',
							   import_payee_name_original='ipno',
							   transaction_date=date(2024, 1, 1))

from datetime import date
from unittest.mock import MagicMock

import pytest

from ynabmemoparser.models import OriginalTransaction, Category, Payee, TransactionModifier, ModifiedTransaction


@pytest.fixture(scope="function")
def mock_original(request):
	try:
		subs = request.param
	except AttributeError as e:
		subs = []
	return OriginalTransaction(id='id',
							   memo='memo',
							   transaction_date=date(2024, 1, 1),
							   amount=1000,
							   category=Category(id='c_id', name='c_name'),
							   payee=Payee(id='p_id', name='p_name', transfer_account_id='t_id'),
							   flag_color='green',
							   import_payee_name='ip_name',
							   import_payee_name_original='ipno_name',
							   subtransactions=frozenset(subs))


@pytest.mark.parametrize('test_attribute, test_input', [
	('memo', 'memox'),
	('transaction_date', date(2024, 1, 2)),
	('category', Category(id='c_id1', name='c_name1')),
	('payee', Payee(id='p_id1', name='p_name1', transfer_account_id='t_id1')),
	('flag_color', 'red'),
	('subtransactions', [MagicMock()])])
def test_is_changed_true(test_attribute, test_input, mock_original):
	# Arrange
	mock_modifier = TransactionModifier.from_original_transaction(mock_original)
	mock_modifier.__setattr__(test_attribute, test_input)
	modified = ModifiedTransaction(original_transaction=mock_original, transaction_modifier=mock_modifier)

	# Act

	r = modified.is_changed()
	assert r is True


def test_changed_false(mock_original):
	# Arrange
	mock_modifier = TransactionModifier.from_original_transaction(mock_original)
	modified = ModifiedTransaction(original_transaction=mock_original, transaction_modifier=mock_modifier)

	# Act
	r = modified.is_changed()
	assert r is False

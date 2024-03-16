from datetime import date
from unittest.mock import MagicMock

import pytest
from pydantic import ValidationError

from ynabmemoparser.models import OriginalTransaction, Category, Payee, TransactionModifier, ModifiedTransaction, OriginalSubTransaction, SubTransaction


@pytest.mark.parametrize('test_attribute, test_input', [
	('memo', 'memox'),
	('transaction_date', date(2024, 1, 2)),
	('category', Category(id='c_id1', name='c_name1')),
	('payee', Payee(id='p_id1', name='p_name1', transfer_account_id='t_id1')),
	('flag_color', 'blue')])
def test_is_changed_true(test_attribute, test_input, mock_original_transaction):
	# Arrange
	mock_modifier = TransactionModifier.from_original_transaction(mock_original_transaction)
	mock_modifier.__setattr__(test_attribute, test_input)
	modified = ModifiedTransaction(original_transaction=mock_original_transaction, transaction_modifier=mock_modifier)

	# Act

	r = modified.is_changed()
	assert r is True


def test_changed_false(mock_original_transaction):
	# Arrange
	mock_modifier = TransactionModifier.from_original_transaction(mock_original_transaction)
	modified = ModifiedTransaction(original_transaction=mock_original_transaction, transaction_modifier=mock_modifier)

	# Act
	r = modified.is_changed()
	assert r is False


@pytest.mark.parametrize('mock_original_transaction', [True], indirect=True)
def test_invalid_subtransactions(mock_original_transaction, mock_subtransaction):
	# Arrange
	mock_modifier = TransactionModifier.from_original_transaction(mock_original_transaction)
	mock_modifier.subtransactions = [mock_subtransaction, mock_subtransaction]
	with pytest.raises(ValidationError):
		ModifiedTransaction(original_transaction=mock_original_transaction, transaction_modifier=mock_modifier)

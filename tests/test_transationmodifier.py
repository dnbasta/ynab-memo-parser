from datetime import date, datetime
from unittest.mock import MagicMock

import pytest
from pydantic import ValidationError

from ynabmemoparser.models import TransactionModifier, Payee, Category, SubTransaction


@pytest.fixture
def mock_modifier(request):
	return TransactionModifier(memo='memo',
							   payee=Payee(name='pname'),
							   category=Category(name='cname', id='cid'),
							   flag_color='red',
							   subtransactions=[],
							   transaction_date=date(2024, 1, 1))


@pytest.fixture
def mock_subtransaction():
	return SubTransaction(memo='memo', payee=Payee(name='pname'), category=Category(name='cname', id='cid'), amount=500)


@pytest.mark.parametrize('test_attr, test_value', [
	('memo', 1),
	('payee', None),
	('payee', 'xxx'),
	('category', None),
	('category', 'xxx'),
	('flag_color', 'brown'),
	# ('subtransactions', [SubTransaction(memo='memo',
	# 									payee=Payee(name='pname'),
	# 									category=Category(name='cname', id='cid'),
	# 									amount=500)]),
	('subtransactions', ['xxx', 'xxx']),
	('transaction_date', 'xxx')
])
def test_invalid_types(test_attr, test_value, mock_modifier):
	# Arrange

	# Act
	mock_modifier.__setattr__(test_attr, test_value)
	with pytest.raises(ValidationError):
		TransactionModifier.model_validate(mock_modifier.__dict__)


def test_invalid_subtransactions(mock_modifier, mock_subtransaction):
	# Arrange
	mock_modifier.subtransactions = [mock_subtransaction]
	with pytest.raises(ValidationError):
		TransactionModifier.model_validate(mock_modifier.__dict__)


@pytest.mark.parametrize('test_attr, test_value', [
	('memo', None),
	('flag_color', None),
	('transaction_date', datetime(2024, 1, 1))
])
def test_valid(test_attr, test_value, mock_modifier):
	# Arrange
	mock_modifier.__setattr__(test_attr, test_value)
	# Assert
	TransactionModifier.model_validate(mock_modifier.__dict__)


def test_valid_subtransactions(mock_modifier, mock_subtransaction):
	mock_modifier.subtransactions = [mock_subtransaction, mock_subtransaction]
	TransactionModifier.model_validate(mock_modifier.__dict__)
	mock_modifier.subtransactions = [mock_subtransaction, mock_subtransaction, mock_subtransaction]
	TransactionModifier.model_validate(mock_modifier.__dict__)

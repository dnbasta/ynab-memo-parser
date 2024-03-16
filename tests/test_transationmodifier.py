from datetime import date, datetime
from unittest.mock import MagicMock

import pytest
from pydantic import ValidationError

from ynabmemoparser.models import TransactionModifier, Payee, Category, SubTransaction


@pytest.fixture
def mock_modifier(request):
	try:
		subs = request.param
	except AttributeError:
		subs = False
	return TransactionModifier(memo='memo',
							   payee=MagicMock(spec=Payee),
							   category=MagicMock(spec=Category),
							   flag_color='red',
							   subtransactions=[],
							   transaction_date=date(2024, 1, 1),
							   original_is_split=subs
							   )


@pytest.mark.parametrize('test_attr, test_value', [
	('memo', 1),
	('payee', None),
	('payee', 'xxx'),
	('category', None),
	('category', 'xxx'),
	('flag_color', 'brown'),
	('subtransactions', [MagicMock(spec=SubTransaction)]),
	('subtransactions', ['xxx', 'xxx']),
	('transaction_date', 'xxx')
])
def test_invalid_types(test_attr, test_value, mock_modifier):
	# Arrange

	# Act
	mock_modifier.__setattr__(test_attr, test_value)
	with pytest.raises(ValidationError):
		TransactionModifier.model_validate(mock_modifier.__dict__)


@pytest.mark.parametrize('mock_modifier', [True], indirect=True)
def test_invalid_subtransactions(mock_modifier):
	# Arrange
	mock_modifier.subtransactions = [MagicMock(spec=SubTransaction), MagicMock(spec=SubTransaction)]
	with pytest.raises(ValidationError):
		TransactionModifier.model_validate(mock_modifier.__dict__)


@pytest.mark.parametrize('test_attr, test_value', [
	('memo', None),
	('flag_color', None),
	('subtransactions', [MagicMock(spec=SubTransaction), MagicMock(spec=SubTransaction)]),
	('subtransactions', [MagicMock(spec=SubTransaction), MagicMock(spec=SubTransaction), MagicMock(spec=SubTransaction)]),
	('transaction_date', datetime(2024, 1, 1))
])
def test_valid(test_attr, test_value, mock_modifier):
	# Arrange
	mock_modifier.__setattr__(test_attr, test_value)
	# Assert
	TransactionModifier.model_validate(mock_modifier.__dict__)

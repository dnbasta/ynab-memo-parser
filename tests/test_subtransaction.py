import pytest
from pydantic import ValidationError

from ynabmemoparser.models import SubTransaction, Category, Payee

@pytest.fixture
def mock_category():
	return Category(name='cname', id='id')


@pytest.fixture
def mock_payee():
	return Payee(name='pname')


def test_subtransaction_success(mock_category, mock_payee):
	SubTransaction(memo='memo', amount=1000, category=mock_category, payee=mock_payee)
	SubTransaction(memo=None, amount=1000, category=mock_category, payee=mock_payee)


def test_subtransaction_error(mock_category, mock_payee):
	with pytest.raises(ValidationError):
		SubTransaction(memo='memo', amount=2.3, payee=mock_payee, category=mock_category)
	with pytest.raises(ValidationError):
		SubTransaction(memo='memo', amount=0, payee=mock_payee, category=mock_category)
	with pytest.raises(ValidationError):
		SubTransaction(memo='memo', amount=0, payee='xxx', category=mock_category)
	with pytest.raises(ValidationError):
		SubTransaction(memo='memo', amount=0, payee=mock_payee, category='xxx')

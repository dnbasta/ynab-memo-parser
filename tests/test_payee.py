import pytest
from pydantic import ValidationError

from ynabmemoparser.models import Payee


def test_payee_success():
	Payee(id='id', name='name')
	Payee(name='name')
	Payee(name=None)
	Payee(name='name', id='id', transfer_account_id='tid')


def test_payee_fail():
	with pytest.raises(ValidationError):
		Payee(id=2, name='name')
	with pytest.raises(ValidationError):
		Payee(name=2)
	with pytest.raises(ValidationError):
		Payee(name='name', transfer_account_id=2)


def test_payee_frozen():
	with pytest.raises(ValidationError):
		payee = Payee(name='name')
		payee.transfer_account_id = 'tid'

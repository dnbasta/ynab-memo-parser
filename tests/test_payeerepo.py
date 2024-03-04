from unittest.mock import MagicMock

import pytest

from ynabmemoparser.exceptions import NoMatchingPayeeError
from ynabmemoparser.models.payee import Payee
from ynabmemoparser.repos.payeerepo import PayeeRepo


def test_fetch_payee_by_name_success():
	# Arrange
	pr = PayeeRepo(client=MagicMock())
	pr._payees = [Payee(id='p_id', name='p_name', transfer_account_id=None)]

	# Act
	p = pr.fetch_payee_by_name(payee_name='p_name')

	# Assert
	assert isinstance(p, Payee)
	assert p.name == 'p_name'


def test_fetch_payee_by_name_fail():
	# Arrange
	pr = PayeeRepo(client=MagicMock())
	pr._payees = [Payee(id='p_id', name='p_name', transfer_account_id=None)]

	# Act
	with pytest.raises(NoMatchingPayeeError):
		pr.fetch_payee_by_name(payee_name='xxx')

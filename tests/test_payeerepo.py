from unittest.mock import MagicMock

import pytest

from ynabmemoparser.exceptions import NoMatchingPayeeError
from ynabmemoparser.models.payee import Payee
from ynabmemoparser.repos.payeerepo import PayeeRepo

@pytest.fixture
def mock_payee_repo():
	return PayeeRepo(payees=[Payee(id='p_id', name='p_name', transfer_account_id=None),
							 Payee(id='p_id', name='p_name', transfer_account_id='transfer_id')])


def test_fetch_payee_by_name_success(mock_payee_repo):
	# Act
	p = mock_payee_repo.fetch_payee_by_name(payee_name='p_name')

	# Assert
	assert isinstance(p, Payee)
	assert p.name == 'p_name'


def test_fetch_payee_by_name_fail(mock_payee_repo):
	# Act
	with pytest.raises(NoMatchingPayeeError):
		mock_payee_repo.fetch_payee_by_name(payee_name='xxx')

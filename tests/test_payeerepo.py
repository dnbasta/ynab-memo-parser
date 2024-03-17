import pytest

from ynabmemoparser.exceptions import NoMatchingPayeeError
from ynabmemoparser.models.payee import Payee
from ynabmemoparser.repos.payeerepo import PayeeRepo


@pytest.fixture
def mock_payee_repo():
	return PayeeRepo(payees=[Payee(id='pid1', name='pname1', transfer_account_id=None),
							 Payee(id='pid2', name='pname2', transfer_account_id='transfer_id')])


def test_fetch_payee_by_name_success(mock_payee_repo):
	# Act
	p = mock_payee_repo.fetch_by_name(payee_name='pname2')

	# Assert
	assert isinstance(p, Payee)
	assert p.name == 'pname2'


def test_fetch_payee_by_name_fail(mock_payee_repo):
	# Act
	with pytest.raises(NoMatchingPayeeError):
		mock_payee_repo.fetch_by_name(payee_name='xxx')


def test_fetch_by_transfer_account_id_success(mock_payee_repo):
	# Act
	r = mock_payee_repo.fetch_by_transfer_account_id('transfer_id')
	assert isinstance(r, Payee)
	assert r.id == 'pid2'


def test_fetch_by_transfer_account_id_fail(mock_payee_repo):
	# Act
	with pytest.raises(NoMatchingPayeeError):
		mock_payee_repo.fetch_by_transfer_account_id('xxx')

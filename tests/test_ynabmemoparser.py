from datetime import date
from unittest.mock import patch, MagicMock

import pytest

from ynabmemoparser import Parser, YnabMemoParser
from ynabmemoparser.exceptions import ParserError
from ynabmemoparser.models import ModifiedTransaction, OriginalTransaction, Category, Payee


@pytest.fixture
@patch('ynabmemoparser.ynabmemoparser.Client')
def mock_memo_parser(mock_client):
	return YnabMemoParser(budget='budget', account='account', token='token')


@pytest.fixture
def mock_transaction():
	return OriginalTransaction(id='id',
							   memo='memo',
							   category=Category(id='cid', name='cname'),
							   payee=Payee(id='pid', name='pname'),
							   subtransactions=frozenset([]),
							   flag_color='red',
							   amount=1000,
							   import_payee_name='ipn',
							   import_payee_name_original='ipno',
							   transaction_date=date(2024, 1, 1))


def test_parse_transactions_fails(mock_memo_parser, caplog, mock_transaction):
	# Arrange
	class MyParser(Parser):
		def parse(self, original, modifier):
			modifier.memo = 'xxx'/0
			return modifier

	# Act
	with pytest.raises(ParserError):
		mock_memo_parser.parse_transactions(transactions=[mock_transaction], parser_class=MyParser)


def test_parse_transactions_success(mock_memo_parser, caplog, mock_transaction):
	# Arrange
	class MyParser(Parser):
		def parse(self, original, modifier):
			modifier.memo = 'xxx'
			return modifier

	# Act
	r = mock_memo_parser.parse_transactions(transactions=[mock_transaction], parser_class=MyParser)
	assert len(r) == 1
	assert isinstance(r[0], ModifiedTransaction)
	assert r[0].transaction_modifier.memo == 'xxx'

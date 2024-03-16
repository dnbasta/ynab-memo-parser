import pytest
from pydantic import ValidationError

from ynabmemoparser.models import Category


def test_category_success():
	Category(name='name', id=None)
	Category(name='name', id='id')


def test_category_error():
	with pytest.raises(ValidationError):
		Category(name=2, id='id')
	with pytest.raises(ValidationError):
		Category(name=None, id='id')
	with pytest.raises(ValidationError):
		Category(name='name', id=2)


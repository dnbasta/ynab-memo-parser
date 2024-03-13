import pytest

from ynabmemoparser.exceptions import NoMatchingCategoryError, MultipleMatchingCategoriesError
from ynabmemoparser.models import CategoryGroup
from ynabmemoparser.models.category import Category
from ynabmemoparser.repos.categoryrepo import CategoryRepo


@pytest.fixture
def mock_category_repo():
	return CategoryRepo(categories=[
		CategoryGroup(name='group1', categories=frozenset([Category(id='c_id', name='c_name')])),
		CategoryGroup(name='group2', categories=frozenset([Category(id='c_id', name='c_name')]))])


def test_fetch_by_name_success(mock_category_repo):
	c = mock_category_repo.fetch_by_name(category_name='c_name', group_name='group1')
	assert c.name == 'c_name'


@pytest.mark.parametrize('test_input, expected', [('xxx', NoMatchingCategoryError),
												  ('c_name', MultipleMatchingCategoriesError)])
def test_fetch_by_name_fail(test_input, expected, mock_category_repo):
	with pytest.raises(expected):
		mock_category_repo.fetch_by_name(category_name=test_input)


def test_fetch_by_id_success(mock_category_repo):
	c = mock_category_repo.fetch_by_id(category_id='c_id')
	assert c.name == 'c_name'


def test_fetch_by_id_fail(mock_category_repo):
	with pytest.raises(NoMatchingCategoryError):
		mock_category_repo.fetch_by_id(category_id='xxx')

from unittest.mock import MagicMock

import pytest

from ynabmemoparser.exceptions import NoMatchingCategoryError, MultipleMatchingCategoriesError
from ynabmemoparser.models.category import Category, CategoryGroup
from ynabmemoparser.repos.categoryrepo import CategoryRepo


def test_fetch_by_name_success():
	cr = CategoryRepo(client=MagicMock())
	cr.category_groups = [CategoryGroup(id='cg_id', name='cg_name',
									   categories=frozenset([Category(id='c_id', name='c_name')]))]
	c = cr.fetch_by_name(category_name='c_name')
	assert c.name == 'c_name'


@pytest.mark.parametrize('test_input, expected', [('xxx', NoMatchingCategoryError),
												  ('c_name', MultipleMatchingCategoriesError)])
def test_fetch_by_name_fail(test_input, expected):
	cr = CategoryRepo(client=MagicMock())
	cr.category_groups = [CategoryGroup(id='cg_id', name='cg_name',
									   categories=frozenset([Category(id='c_id', name='c_name')])),
						  CategoryGroup(id='cg_id2', name='cg_name2',
										categories=frozenset([Category(id='c_id2', name='c_name')]))
						  ]
	with pytest.raises(expected):
		cr.fetch_by_name(category_name=test_input)


def test_fetch_by_id_success():
	cr = CategoryRepo(client=MagicMock())
	cr.category_groups = [CategoryGroup(id='cg_id', name='cg_name',
									   categories=frozenset([Category(id='c_id', name='c_name')]))]
	c = cr.fetch_by_id(category_id='c_id')
	assert c.name == 'c_name'


def test_fetch_by_id_fail():
	cr = CategoryRepo(client=MagicMock())
	cr.category_groups = [CategoryGroup(id='cg_id', name='cg_name',
									   categories=frozenset([Category(id='c_id', name='c_name')]))]
	with pytest.raises(NoMatchingCategoryError):
		cr.fetch_by_id(category_id='xxx')

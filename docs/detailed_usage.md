# Detailed Usage
## Change the category
The parser allows changing the category of the transaction. It comes with a [`CategoryRepo`][repos.CategoryRepo] 
instance attached which can be used in the parser via `self.categories`. The repo can be called with either 
`fetch_by_name()` or `fetch_by_id()` method to fetch a valid category. Using the repo is recommended to ensure you only
assign valid categories to the modifier. The library doesn't allow creating new categories and specifying a 
non-existing category will raise an error.
```py
from ynabmemoparser import Parser

class MyParser(Parser):

    def parse(self, original, modifier):
        my_category = self.categories.fetch_by_name('my_category')
        # or alternatively
        my_category = self.categories.fetch_by_id('category_id')
        modifier.category = my_category
        
        return modifier
```
The [`CategoryRepo`][repos.CategoryRepo] instance gets build when the library get initialized and can also be accessed 
from the main instance (e.g. for finding category ids to be used in the parser later). 

```py
from ynabmemoparser import YnabMemoParser
    ynab_memo_parser = YnabMemoParser(token='<token>', budget='<budget>', account='<account>')
    # fetches all categories and returns a dict with group name as key and list of categories as values
    categories = ynab_memo_parser.categories.fetch_all()
```

## Change the payee
The payee of the transaction can be changed either by creating a new [`Payee`][models.Payee] object or fetching an
existing payee from the [`PayeeRepo`][repos.PayeeRepo] which can be used in the parser via `self.payees`. The repo can 
be called with either `fetch_by_name()` or `fetch_by_id()` method to fetch an existing payee. It can also be called with
`fetch_by_transfer_account_id()` to fetch a transfer payee. You can find the account id for the transfer account 
following the method mentioned in the [preparations](#preparations) section.

```py
from ynabmemoparser import Parser
from ynabmemoparser.models import Payee

class MyParser(Parser):

    def parse(self, original, modifier):
        my_payee = Payee(name='My Payee')
        # or 
        my_payee = self.payees.fetch_by_name('My Payee')
        # or 
        my_payee = self.payees.fetch_by_id('payee_id')
        # or for transfers
        my_payee = self.payees.fetch_by_transfer_account_id('transfer_account_id')
        modifier.payee = my_payee
        
        return modifier
```
The [`PayeeRepo`][repos.PayeeRepo] instance gets build when the library get initialized and can also be accessed 
from the main instance. 

```py
from ynabmemoparser import YnabMemoParser
    ynab_memo_parser = YnabMemoParser(token='<token>', budget='<budget>', account='<account>')
    # fetches all payees in the budget
    payees = ynab_memo_parser.payees.fetch_all()
```

## Split the transaction
The transaction can be splitted if the original transaction is not already a split (YNAB doesn't allow updating splits 
of an existing split transaction). Splits can be created by using [`SubTransaction`][models.SubTransaction] instances.
There must be at least two subtransactions and the sum of their amounts must be equal to the amount of the original 
transaction.
```py
from ynabmemoparser import Parser
from ynabmemoparser.models import SubTransaction

class MyParser(Parser):

    def parse(self, original, modifier):
        # example for splitting a transaction in two equal amount subtransactions with different categories 
        subtransaction_1 = SubTransaction(amount=original.amount / 2,
                                          category=original.category)
        subtransaction_2 = SubTransaction(amount=original.amount / 2, 
                                          category=self.categories.fetch_by_name('My 2nd Category'))
        modifier.subtransactions = [subtransaction_1, subtransaction_2]
        
        return modifier
```



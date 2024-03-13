# Installation and Usage

This library helps you to use original memo and payee information from your bank transactions to either show additional
details or substitute/change the current one in YNAB. It can be helpful for cases in which YNAB import does not handle the 
information coming from the bank well (e.g. not showing the actual bank memo or populating a wrong payee name).

[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/dnbasta)

## Preparations
1. Create a personal access token for YNAB as described [here](https://api.ynab.com/)
2. Get the IDs of your budget and account which records are faulty. You can find both IDs if you go to 
https://app.ynab.com/ and open the target account by clicking on the name on the left hand side menu. 
The URL does now contain both IDs `https://app.ynab.com/<budget_id>/accounts/<account_id>`

## Installation 
Install library from PyPI
```bash
pip install ynab-memo-parser
```

## Usage
### 1. Fetch current transactions from YNAB and check for useful values
All records in YNAB come with additional information attached which is not shown in the user interface. You find both
values in the `import_payee_name` and `import_payee_name_original` attributes of the returned transactions. All other
information is also available with each transaction record.
```py
from ynabmemoparser import YnabMemoParser

ynab_memo_parser = YnabMemoParser(token='<token>', budget='<budget>', account='<account>')
list_of_transactions = ynab_memo_parser.fetch_transactions()
```

### 2. Create a `Parser` child class which implements your logic
The class needs to implement a `parse()` method which does the actual parsing of a transaction. The method is called
with a `Transaction` object which you can modify to your liking and return.

```py
from ynabmemoparser import Parser
from ynabmemoparser.models import TransactionModifier


class MyParser(Parser):

	def parse(self, transaction: TransactionModifier) -> TransactionModifier:
		# your implementation

		# return your altered transaction
		return transaction
```
The parser has two attributes which you can use for manipulating category and payee of the transaction. 
E.g. you can fetch a [`Category`][models.Category] via the `categories` attribute in the parser class. You can either 
fetch a category by its name, its id (more robust) or a list of categories by the category group name. 
Check the [`CategoryRepo`][repos.CategoryRepo] reference for more details
```py
class MyParser(Parser):

    def parse(self, transaction: Transaction) -> Transaction:
        my_category = self.categories.fetch_by_name('my_category')
        transaction.category = my_category
        return transaction
```
If needed you can also fetch an existing [`Payee`][models.Payee] via the `payees` attribute in the parser class. 
You can either fetch the payee by its name or its id. 
Check the [`PayeeRepo`][repos.PayeeRepo] reference for more details
```py
class MyParser(Parser):

    def parse(self, transaction: Transaction) -> Transaction:
        my_payee = self.categories.fetch_by_name('my_payee')
        transaction.payee = my_payee
        return transaction
```
### 3. Test your parser on some records
Provide your parser class to [`YnabMemoParser`][ynabmemoparser.YnabMemoParser] upon init. The library will initialize your parser and use it inside its
`parse_transactions()` method.
```py
from ynabmemoparser import YnabMemoParser

ynab_memo_parser = YnabMemoParser(token='<token>', 
                                  budget='<budget>', 
                                  account='<account>',
                                  parser_class=MyParser)
original_transactions = ynab_memo_parser.fetch_transactions()
parsed_transactions = ynab_memo_parser.parse_transactions(transactions=original_transactions)
```
You will get back a list of [`Transaction`][models.Transaction] objects. Check the changed attributes of the 
transaction either in your debug tool or call the `as_dict()` helper function of the class.

### 4. Update your records in YNAB
If you are satisfied with your parsing results you can pass the list of the parsed `Transaction` to the 
`update_records()` method. It will update the respective transactions in YNAB and return an integer with the number 
of successfully updated records.
```py
updated_transaction_count = ynab_memo_parser.update_transactions(parsed_transactions)
```

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
with the [`OriginalTransaction`][models.OriginalTransaction] and a [`TransactionModifier`][models.TransactionModifier] 
object which is prefilled with values from the original transaction. Its attributes can be modified and it needs to be 
returned at the end of the function.

```py
from ynabmemoparser import Parser
from ynabmemoparser.models import OriginalTransaction, TransactionModifier


class MyParser(Parser):

	def parse(self, original: OriginalTransaction, modifier: TransactionModifier) -> TransactionModifier:
		# your implementation

		# return the altered modifier
		return modifier
```
The parser has two attributes which can be used for manipulating category and payee of the transaction. 
E.g. you can fetch a [`Category`][models.Category] via the `categories` attribute in the parser class. You can either 
fetch a category by its name, its id (more robust) or fetch a list of categories by the category group name. 
Check the [`CategoryRepo`][repos.CategoryRepo] reference for more details. You can also fetch an existing [`Payee`]
[models.Payee] via the `payees` attribute in the parser class. You can either fetch the payee by its name or its id. 
Check the [`PayeeRepo`][repos.PayeeRepo] reference for more details
```py
class MyParser(Parser):

    def parse(self, original, modifier):
        my_category = self.categories.fetch_by_name('my_category')
        modifier.category = my_category
        
        my_payee = self.categories.fetch_by_name('my_payee')
        modifier.payee = my_payee
        
        return modifier
```

### 3. Test your parser on some records
Provide a list of [`OriginalTransaction`][models.OriginalTransaction] objects and your parser class to the `parse()` 
method of your [`YnabMemoParser`][ynabmemoparser.YnabMemoParser] instance. You will get back a list of 
[`ModifiedTransaction`][models.ModifiedTransaction] objects. Check the changed attributes of the transaction either in 
your debug tool or call the `as_dict()` helper function of the class.
```py
parsed_transactions = ynab_memo_parser.parse_transactions(transactions=list_of_transactions, 
                                                          parser_class=MyParser)
```

### 4. Update your records in YNAB
If you are satisfied with your parsing results you can pass the list of the 
[`ModifedTransaction`][modelf.ModifiedTransaction] objects to the `update_records()` method. It will update actually 
changed transactions in YNAB and return an integer with the number of successfully updated records.
```py
updated_transaction_count = ynab_memo_parser.update_transactions(transactions=parsed_transactions)
```

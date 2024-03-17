# ynab-memo-parser

[![GitHub Release](https://img.shields.io/github/release/dnbasta/ynab-mmo-parser?style=flat)]() 
[![Github Release](https://img.shields.io/maintenance/yes/2100)]()

This library helps you to use original memo and payee information from your bank transactions to either show additional
details or substitute/change the current one in YNAB. It can be helpful for cases in which YNAB import does not handle the 
information coming from the bank well (e.g. not showing the actual bank memo or populating a wrong payee name).

[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/dnbasta)

## Preparations
1. Create a personal access token for YNAB as described [here](https://api.ynab.com/)
2. Get the IDs of your budget and account which records are faulty. You can find both IDs if you go to 
https://app.ynab.com/ and open the target account by clicking on the name on the left hand side menu. 
The URL does now contain both IDs `https://app.ynab.com/<budget_id>/accounts/<account_id>`

## Usage
A detailed documentation is available at https://ynab-memo-parser.readthedocs.io

### Fetch transactions
Fetch current transactions from YNAB backend with all available information and check for useful values. All records 
come with two attributes (`import_payee_name` and `import_payee_name_original`) which are not shown in the user 
interface.
```py
from ynabmemoparser import YnabMemoParser

ynab_memo_parser = YnabMemoParser(token='<token>', budget='<budget>', account='<account>')
orig_transactions = ynab_memo_parser.fetch_transactions()
```

### Create a `Parser` child class
This class is for implementing your actual logic. It needs to implement a `parse()` method which receives on runtime 
the `OriginalTransaction` and a `TransactionModifier`. The 
latter is prefilled with values from the original transaction. Its attributes can be modified and it needs to be 
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

### Test your parser
Test the parser on records fetched via the `fetch_transactions()`method. If only a subset of these transactions should
et parsed, filter them before handing the list over to the `parse_transactions()` method. The method returns a list of 
`ModifiedTransaction` objects which can be inspected for the changed properties.
```py
transations = ynab_memo_parser.fetch_transactions()
# optionally filter transactions before passing them to method below
mod_transactions = ynab_memo_parser.parse_transactions(transactions=transactions,
                                                       parser_class=MyParser)
```

### Update records in YNAB
If you are satisfied with your parsing results you can pass the list of the 
`ModifedTransaction` objects to the `update_records()` method. It will update  
the changed transactions in YNAB and return an integer with the number of successfully updated records.
```py
count = ynab_memo_parser.update_transactions(transactions=mod_transactions)
```

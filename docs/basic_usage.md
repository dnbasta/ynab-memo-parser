# Basic Usage
### Fetch transactions
Fetch current transactions from YNAB backend with all available information and check for useful values. All records 
come with two attributes (`import_payee_name` and `import_payee_name_original`) which are not shown in the user 
interface.
```py
from ynabmemoparser import YnabMemoParser

ynab_memo_parser = YnabMemoParser(token='<token>', budget='<budget>', account='<account>')
orig_transactions = ynab_memo_parser.fetch_transactions()
```

### Create a [`Parser`][parser.Parser] child class
This class is for implementing your actual logic. It needs to implement a `parse()` method which receives on runtime 
the [`OriginalTransaction`][models.OriginalTransaction] and a [`TransactionModifier`][models.TransactionModifier]. The 
latter is prefilled with values from the original transaction. Its attributes can be modified and it needs to be 
returned at the end of the function. Please refer to the [detailed usage](3_detailed_usage.md) section for explanations how
to change different attributes.
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
[`ModifiedTransaction`][models.ModifiedTransaction] objects which can be inspected for the changed properties.
```py
transations = ynab_memo_parser.fetch_transactions()
# optionally filter transactions before passing them to method below
mod_transactions = ynab_memo_parser.parse_transactions(transactions=transactions,
                                                       parser_class=MyParser)
```

### Update records in YNAB
If you are satisfied with your parsing results you can pass the list of the 
[`ModifedTransaction`][models.ModifiedTransaction] objects to the `update_records()` method. It will update  
the changed transactions in YNAB and return an integer with the number of successfully updated records.
```py
count = ynab_memo_parser.update_transactions(transactions=mod_transactions)
```

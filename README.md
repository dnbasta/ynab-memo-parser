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

## Basic Usage
### 1. Install library from PyPI

```bash
pip install ynab-memo-parser
```
### 2. Check your original memo and payee values for potential things to use
All records in YNAB come with their original memo and payee information attached. You can see both values if you use
the `fetch records' function of this library and look at a couple sample records.
```py
from ynabmemoparser import YnabMemoParser

ynab_memo_parser = YnabMemoParser(token='<token>', budget='<budget>', account='<account>')
ynab_memo_parser.fetch_record_dicts()
```
You will get back a dictionary with all data stored for the transaction. The library uses the following keys with the
stated labels
- `import_payee_name_original` as `original_memo`
- `import_payee_name` as `original_payee`
- `payee` as `current_payee`
- `memo` as `current_memo`


### 3. Create a `Parser` child class which implements your logic
The class needs to implement a logic for `parse_payee()` and `parse_memo()` based on the values coming from the four 
fields above. If you don't want to change anything in the field you e.g. just `return current_payee` inside the 
`parse_payee()` function. 

```py
from ynabmemoparser import Parser

class MyParser(Parser):

    def parse_payee(self, original_payee: str, current_payee: str, original_memo: str, current_memo: str) -> str:
        # your implementation

    def parse_memo(self, original_payee: str, current_payee: str, original_memo: str, current_memo: str) -> str:
        # your implementation

```
### 3. Test your parser on some records
```py
from ynabmemoparser import YnabMemoParser

ynab_memo_parser = YnabMemoParser(token='<token>', budget='<budget>', account='<account>')
record_dicts = ynab_memo_parser.fetch_record_dicts()
parsed_records = ynab_memo_parser.parse_records(records_dicts=record_dicts, parser=MyParser())
```
You will get back a list of `YnabRecord` objects. Check the `payee` and `memo` fields in these objects to see the result
of your parser.

### 4. Update your records in YNAB
If you are satisfied with your parsing results you can pass the list of `YnabRecord` to the `update_records()`function.
It will update the `payee`and `memo` values in YNAB with the values in the `YnabRecord` object
```py
ynab_memo_parser.update_records(parsed_records)
```
If the insert is successful you get back an integer with the number of records which have been updated.



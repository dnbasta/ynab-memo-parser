# Installation

This library helps you to use original memo and payee information from your bank transactions to either show additional
details or substitute/change the current one in YNAB. It can be helpful for cases in which YNAB import does not handle the 
information coming from the bank well (e.g. not showing the actual bank memo or populating a wrong payee name).

[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/dnbasta)

## Preparations
1. Create a personal access token for YNAB as described [here](https://api.ynab.com/)
2. Get the IDs of your budget and account which records are faulty. You can find both IDs if you go to the
[YNAB Webapp](https://app.ynab.com/) and open the target account by clicking on the name on the left hand side menu. 
The URL does now contain both IDs `https://app.ynab.com/<budget_id>/accounts/<account_id>`

## Installation 
Install library from PyPI
```bash
pip install ynab-memo-parser
```

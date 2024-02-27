from ynabmemoparser.parser import Parser
from ynabmemoparser.ynabrecord import YnabRecord


class RecordBuilder:

	def __init__(self, parser: Parser):
		self._parser = parser

	def build(self, t_dict: dict) -> YnabRecord:
		original_memo = t_dict['import_payee_name_original']
		original_payee = t_dict['import_payee_name']
		current_payee = t_dict['payee_name']
		current_memo = t_dict['memo']
		payee = self._parser.parse_payee(original_payee=original_payee,
								 		 current_payee=current_payee,
										 original_memo=original_memo,
										 current_memo=current_memo)
		memo = self._parser.parse_memo(original_payee=original_payee,
								 		 current_payee=current_payee,
										 original_memo=original_memo,
										 current_memo=current_memo)

		return YnabRecord(id=t_dict['id'],
				   original_memo=original_memo,
				   current_memo=current_memo,
				   original_payee=original_payee,
				   current_payee=current_payee,
				   memo=memo,
				   payee=payee)


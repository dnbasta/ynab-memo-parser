from abc import abstractmethod


class Parser:

	@abstractmethod
	def parse_payee(self, original_payee: str, current_payee: str, original_memo: str, current_memo: str) -> str:
		pass

	@abstractmethod
	def parse_memo(self, original_payee: str, current_payee: str, original_memo: str, current_memo: str) -> str:
		pass

from dataclasses import dataclass


@dataclass
class YnabRecord:
	id: str
	memo: str
	payee: str
	original_memo: str
	original_payee: str
	current_memo: str
	current_payee: str

	def as_dict(self):
		return dict(id=self.id, memo=self.memo, payee_name=self.payee)

	def changed(self) -> bool:
		if self.memo != self.current_memo or self.payee != self.current_payee:
			return True
		return False

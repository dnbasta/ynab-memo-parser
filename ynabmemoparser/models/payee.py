from dataclasses import dataclass


@dataclass(frozen=True)
class Payee:
	name: str
	id: str




class Summoner():
	def __init__(self, data: dict):
		print(f" Initializing Summoner {data['name']}")
		self._data = data

	def raw_data(self) -> dict:
		""" raw dictionary data """
		return self._data
	
	def name(self) -> str:
		""" summoner name of account """
		return self._data['name']

	def puuid(self) -> str:
		""" puuid of account, unqiue """
		return self._data['puuid']

	def accountId(self) -> str:
		""" accont id of account """
		return self._data['accountId']

	def summonerId(self) -> str:
		""" summoner id of account """
		return self._data['id']

	def revision_date(self) -> int:
		""" returns revision date as epoch milliseconds """
		return self._data['revisionDate']


	def __str__(self):
		return f'Summoner: {self._data["name"]} (Lv. {self._data["summonerLevel"]})'


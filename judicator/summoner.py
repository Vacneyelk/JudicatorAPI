


class Summoner():
	def __init__(self, data: dict):
		print(f" Initializing Summoner {data['name']}")
		self._data = data

	def raw_data(self):
		return self._data
	
	def name(self):
		return self._data['name']

	def puuid(self):
		return self._data['puuid']

	def accountId(self):
		return self._data['accountId']

	def summonerId(self):
		return self._data['id']

	def revision_date(self):
		return self._data['revisionDate']


	def __str__(self):
		return f'Summoner: {self._data["name"]} (Lv. {self._data["summonerLevel"]})'


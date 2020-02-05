

class League:
	def __init__(self, data: dict):
		self._data = data

	def raw_data(self):
		return self._data

	def summoner_name(self):
		return self._data['summonerName']

	def summoner_id(self):
		return self._data['summonerId']

	def tier(self):
		return self._data['tier']

	def rank(self):
		return self._data['rank']

	def queue_type(self):
		return self._data['queueType']

	def wins(self):
		return self._data['wins']

	def losses(self):
		return self._data['losses']

	def __str__(self):
		return f"League: ({self._data['summonerName']}, {self._data['queueType']})"

	def __repr__(self):
		return str(self)
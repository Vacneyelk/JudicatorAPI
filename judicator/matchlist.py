

class MatchList:
	"""
		Class for MatchList object
		Object contains
			* champion : int
			* gameId : int
			* lane : str
			* platformId : str
			* queue : int
			* role : str
			* season : int
			* timestamp : int
	"""

	def __init__(self, data: list):
		self._data = data

	def raw_data(self):
		return self._data

	def add_matches(self, matches: list):
		self._data.extend(matches)

	def matches(self) -> list:
		return self._data

	def __str__(self):
		return f"Matchlist: game count -> {len(self)}"

	def __len__(self):
		return len(self._data)
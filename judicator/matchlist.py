from judicator.match import Match

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

	def __init__(self, data: list=None):
		if data is None:
			self._data = []
		else:
			self._data = data

	def raw_data(self) -> list:
		""" returns raw matchlist """
		return self._data

	def add_matches(self, matches: list) -> None:
		""" extends existing matches """
		self._data.extend(matches)

	def matches(self) -> [Match]:
		""" returns list of Match objects """
		return [Match(item) for item in self._data]

	def __str__(self):
		return f"Matchlist: game count -> {len(self)}"

	def __len__(self):
		return len(self._data)



class Match:
	def __init__(self, data: dict):
		self._data = data

	def raw_data(self) -> dict:
		""" raw dictionary data """
		return self._data

	def season_id(self) -> int:
		""" season id of the game """
		return self._data['seasonId']

	def queue_id(self) -> int:
		""" queue id of the game """
		return self._data['queueId']

	def game_id(self) -> int:
		""" match id of the game """
		return self._data['gameId']

	def game_version(self) -> str:
		""" version of the game match was played on """
		return self._data['gameVersion']

	def game_duration(self) -> int:
		""" duration of the game in seconds """
		return self._data['gameDuration']

	def participant_account_ids(self) -> list:
		"""
			Retrieves a list of current account ids for the game

			Returns:
				list of current account ids (strings)
		"""
		return [ part['player']['currentAccountId'] for part in self._data['participantIdentities'] ]

	def __str__(self):
		return f"Match: {self._data['gameId']}"

	def __repr__(self):
		return str(self)



class Match:
	def __init__(self, data: dict):
		self._data = data

	def raw_data(self):
		return self._data

	def season_id(self):
		return self._data['seasonId']

	def queue_id(self):
		return self._data['queueId']

	def game_id(self):
		return self._data['game_id']

	def game_version(self):
		return self._data['gameVersion']

	def game_duration(self):
		return self._data['gameDuration']

	def participant_account_ids(self):
		"""
			Retrieves a list of current account ids for the game

			Returns:
				list of current account ids
		"""
		return [ part['player']['currentAccountId'] for part in self._data['participantIdentities'] ]

	def __str__(self):
		return f"Match: {self._data['gameId']}"

	def __repr__(self):
		return str(self)
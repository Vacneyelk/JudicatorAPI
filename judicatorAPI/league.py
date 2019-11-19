import endpoints as ep
import credentials

from api_util import get_request

_API_PARAM = {
	'api_key' : credentials.API_KEY
}

class League:
	def __init__(self, data):
		self._data = data

def get_summoner_league(summoner_id: str) -> League:
	"""
		Gets the league information for a summoner.
		Information included is rank, leagueId, hotStreak, queueType, among other information.
		Check Riot API for more details.

		Args
			summoner_id: should be the encrypted summoner_id for an account

		Returns
			League class object that contains the necessary data
	"""
	rsp = get_request(
			f'https://{ep.EP_NA}{ep.EP_LEAGUE_BY_SUMMONER}{summoner_id}',
			params=_API_PARAM
		)
	return League(rsp.json())

if __name__ == '__main__':
	# Pobeaver summoner id
	# MJerabWNPDBcYCLDPETqFgLKWLZLLUUg6YcSfm_2vgTlqb4
	from pprint import pprint

	result = get_summoner_league('MJerabWNPDBcYCLDPETqFgLKWLZLLUUg6YcSfm_2vgTlqb4')
	for item in result._data:
		pprint(result._data)
	# print(result._data)

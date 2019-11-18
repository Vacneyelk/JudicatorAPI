
from itertools import chain

import endpoints as ep
import credentials

from api_util import get_request
from api_logging import japi_log

_API_PARAM = {
	'api_key' : credentials.API_KEY
}

class MatchList:
	"""
		Each match entry contains
			* champion : int
			* gameId : int
			* lane : str
			* platformId : str
			* queue : int
			* role : str
			* season : int
			* timestamp : int
	"""
	# TODO: create more interesting match list class with filtering matches
	def __init__(self, data):
		self._data = data

	def get_matches(self) -> list:
		""" returns a list of match reference dictionaries """
		return self._data

class Match:
	def __init__(self, data):
		self._data = data

	def season_id(self) -> int:
		return self._data['seasonId']

	def queue_id(self) -> int:
		return self._data['queueId']

	def game_id(self) -> int:
		return self._data['gameId']

	def game_duration(self) -> int:
		return self._data['gameDuration']

	def participant_account_ids(self, debug: bool=False) -> list:
		""" 
			gets a list of account ids in the game 
			NOTE: account ids my no longer be valid
		"""
		account_ids = [ part['player']['currentAccountId'] for part in self._data['participantIdentities'] ]
		japi_log.debug(f'Pulling account ids: {account_ids}')
		return account_ids

	def __str__(self):
		return f"Match: {self._data['gameId']}"

	def __repr__(self):
		return str(self)



"""
	General Notes for matchlist from API
	If beginIndex but no endIndex, endIndex = beginIndex+100
	If endIndex but no beginIndex, beginIndex = 0
	Max range of 100
	> only specifying endTime may result in 400 error due to range over 100

	endTime > beginTime or 400 error
	Max time range = 1 week
"""
def get_matchlist(account_id: str, champion: list = None, queue: list = None, season: list = None, end_time: int = None, begin_time: int = None, end_index: int = None, begin_index: int = 0):
	"""
		Gets the matchlist for an account
		If only the account is specified then all matches will be returned

		If extra parameters are given then matches will be filtered according. Check https://developer.riotgames.com/apis#match-v4/GET_getMatchlist for more details

		TODO: mess with Set[int] parameters (champion, queue, season)

		Args
			account_id:
			champion:
			queue:
			season:
			end_time:
			begin_time:
			end_index:
			begin_index:

		Return
			list of matches
	"""
	parameters = _API_PARAM.copy()
	if champion is not None:
		parameters['champion'] = champion
	if queue is not None:
		parameters['queue'] = queue
	if season is not None:
		parameters['season'] = season
	if end_time is not None:
		parameters['endTime'] = end_time
	if begin_time is not None:
		parameters['beginTime'] = begin_time
	if end_index is not None:
		parameters['endIndex'] = end_index
	if begin_index is not None:
		parameters['beginIndex'] = begin_index
	# print(parameters)
	
	match_lists = []
	while not match_lists or len(match_lists[-1]) >= 100:
		rsp = get_request(
				f'https://{ep.EP_NA}{ep.EP_MATCHLIST_BY_ACCOUNT}{account_id}',
				parameters
			)
		match_lists.append(rsp.json()['matches'])
		parameters['beginIndex'] = rsp.json()['endIndex']
		
	match_list = list(chain(*match_lists))
	return match_list

def get_match(match_id: str):
	"""
		
	"""
	rsp = get_request(
			f'https://{ep.EP_NA}{ep.EP_MATCH_MATCHES}{match_id}',
			_API_PARAM
		)
	return Match(rsp.json())



if __name__ == '__main__':
	pass
	# PoBeaver Account ID
	pobeaver_aid = 'OGmWKgOAk_k0iqZFuj-XUdfpfK7-qDLMtokjvU9w-aw_jw'
	# rsp = get_request(f'https://{ep.EP_NA}{ep.EP_MATCHLIST_BY_ACCOUNT}{pobeaver_aid}', _API_PARAM)
	from pprint import pprint
	matches = get_matchlist(pobeaver_aid, queue=['420'])
	pprint(matches)
	# pprint(dict(rsp.json()))
	# pprint(get_matchlist(pobeaver_aid, queue=['420']))
	# m = get_match('3172572127')
	# print(m.participant_account_ids())



from judicator.api.base import BaseAPI
from judicator.matchlist import MatchList
from judicator.match import Match

import warnings
from datetime import datetime

class MatchAPI(BaseAPI):
	def __init__(self):
		BaseAPI.__init__(self)
		self.ep_matches_by_matchid = '/lol/match/v4/matches/'
		self.ep_matchlist_by_accountid = '/lol/match/v4/matchlists/by-account/'

	def get_matchlist_by_accountid(self, account_id: str, champions: set=None, queues: set=None, seasons: set=None, end_time: datetime=None, begin_time: datetime=None, end_idx: int=None, begin_idx: int=None, exhaust: bool=False) -> MatchList:
		"""
			# TODO: implement all parameter functionality, see if we can clean up logic (especially loop)
			Gets the matchlist for a user account

			Args:
				account_id: the account id of a summoner
				champions: set of champion ids to filter the matchlist
				queues: set of queue ids to filter the matchlist
				seasons: set of season ids to filter the matchlist
				TODO: Consider conversion to something more robust, datetime?
				======
				Times can be generated with int(datetime.datetime(year, month, day).timestamp()) * 1000
				end_time: end of time range in epoch milliseconds (begin_time required)
				begin_time: beginning of time range in epoch milliseconds (end_time required)
				======
				end_idx: ending index of games, max range is 100
				begin_idx: beinning index of games, max range 100
				exhaust: this will continue requesting games until all matches have been collected
				

			Returns:
				Matchlist object
		"""
		parameters = {}

		if champions is not None: parameters['champion'] = list(champions)
		if queues is not None: parameters['queue'] = list(queues)
		if seasons is not None: parameters['season'] = list(seasons)

		if end_time is not None and begin_time is not None:
			end_time = int(end_time.timestamp()) * 1000
			begin_time = int(begin_time.timestamp()) * 1000
			assert end_time - begin_time <= 604800000, 'Time range must be 604800000 (1 week)'
			parameters['endTime'] = end_time
			parameters['beginTime'] = begin_time
		else:
			assert end_time is None or begin_time is None, 'Both end and begin time must be specified or neither'

		if end_idx is not None and begin_idx is not None:
			assert end_idx - begin_idx <= 100, 'Index range must be < 100'
			assert end_idx > begin_idx, 'end index must be less than beginning index'
			parameters['endIndex'] = end_idx
			parameters['beginIndex'] = begin_idx
		else:
			assert end_idx is None or begin_idx is None, 'Both end and begin index must be specified or neither'

		if exhaust:
			if 'endTime' in parameters: 
				del parameters['endTime']
				warnings.warn('Exhause overwriting endTime parameter')
			if 'beginTime' in parameters: 
				del parameters['beginTime']
				warnings.warn('Exhause overwriting beginTime parameter')
			if 'endIndex' in parameters: 
				del parameters['endIndex']
				warnings.warn('Exhause overwriting endIndex parameter')
			if 'beginIndex' in parameters: 
				del parameters['beginIndex']
				warnings.warn('Exhause overwriting endTime parameter')
			parameters['beginIndex'] = 0

		matches = MatchList()
		while True:
			endpoint = f"{self.ep_matchlist_by_accountid}{account_id}"
			rsp = self._api_call(self.platforms['NA1'], endpoint, parameters)
			new_matches = rsp.json()['matches']
			matches.add_matches(new_matches)
			if exhaust and len(new_matches) >= 100:
				parameters['beginIndex'] = len(matches)
			else:
				break

		return matches

	def get_match_by_matchid(self, match_id: str) -> Match:
		"""
			gets a match by its match id
		"""
		endpoint = f"{self.ep_matches_by_matchid}{match_id}"
		rsp = self._api_call(self.platforms['NA1'], endpoint, {})
		return Match(rsp.json())

if __name__ == '__main__':

	from datetime import datetime
	mapi = MatchAPI()
	aid = 'OGmWKgOAk_k0iqZFuj-XUdfpfK7-qDLMtokjvU9w-aw_jw'
	queues = set([430, 440])

	# end = int(datetime(2020, 3, 26).timestamp()) * 1000
	# begin = int(datetime(2020, 3, 19).timestamp()) * 1000
	# end = 215
	# begin = 200
	# end = datetime(2020, 3, 26)
	# begin = datetime(2020, 3, 19)


	ml = mapi.get_matchlist_by_accountid(aid, end_idx=end, begin_idx=begin)
	
	print(ml)
	games = ml.matches()
	print(games)
	# print(ml._data)

	# ml2 = mapi.get_matchlist_by_accountid(aid, begin_idx=99)
	# print(ml2)
	# games2 = ml2.matches()
	# print(len(games2))

	# from pprint import pprint
	# pprint(games)
	# print('BREAK')
	# pprint(games2)
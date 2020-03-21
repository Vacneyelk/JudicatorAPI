
from judicator.api.base import BaseAPI
from judicator.matchlist import MatchList
from judicator.match import Match


class MatchAPI(BaseAPI):
	def __init__(self):
		BaseAPI.__init__(self)
		self.ep_matches_by_matchid = '/lol/match/v4/matches/'
		self.ep_matchlist_by_accountid = '/lol/match/v4/matchlists/by-account/'

	def get_matchlist_by_accountid(self, account_id: str, champions: set=None, queues: set=None, seasons: set=None, end_time: int=None, begin_time: int=None, end_idx: int=None, begin_idx: int=None, exhaust: bool=False) -> MatchList:
		"""
			# TODO: implement all parameter functionality, see if we can clean up logic (especially loop)
			Gets the matchlist for a user account

			Args:
				account_id: the account id of a summoner
				end_idx: ending index of games, max range is 100
				begin_idx: beinning index of games, max range 100
				seasons: set of season ids to filter the matchlist
				exhaust: this will continue requesting games until all matches have been collected

				NOT IMPLEMENTED
				champions: set of champion ids to filter the matchlist
				queues: set of queue ids to filter the matchlist
				end_time: end of time range?
				begin_time: beginning of time range?
				

			Returns:
				Matchlist object
		"""
		parameters = {}

		if champions is not None or end_time is not None or begin_time is not None:
			raise NotImplementedError

		if queues is not None:
			parameters['queue'] = list(queues)
		if seasons is not None:
			parameters['season'] = list(seasons)
		if end_idx is not None and begin_idx is not None:
			if end_idx - begin_idx > 100:
				raise Exception
			if end_idx <= begin_idx:
				raise Exception
		if end_idx is None:
			parameters['endIndex'] = end_idx
		if begin_idx is not None:
			parameters['beginIndex'] = begin_idx
		else:
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
	mapi = MatchAPI()
	aid = 'OGmWKgOAk_k0iqZFuj-XUdfpfK7-qDLMtokjvU9w-aw_jw'
	queues = set([430, 440])
	ml = mapi.get_matchlist_by_accountid(aid, queues=queues, exhaust=True)
	
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
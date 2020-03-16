
from judicator.api.base import BaseAPI
from judicator.summoner import Summoner

class SummonerAPI(BaseAPI):
	def __init__(self):
		BaseAPI.__init__(self)
		self.ep_summoner_by_accountid = '/lol/summoner/v4/summoners/by-account/'
		self.ep_summoner_by_name = '/lol/summoner/v4/summoners/by-name/'
		self.ep_summoner_by_puuid = '/lol/summoner/v4/summoners/by-puuid/'
		self.ep_summoner_summonerid = '/lol/summoner/v4/summoners/'

	def get_summoner_by_account_id(self, account_id: str) -> Summoner:
		"""
			gets summoner by their account id
		"""
		endpoint = f'{self.ep_summoner_by_accountid}{account_id}'
		rsp = self._api_call(self.platforms['NA1'], endpoint, {})
		return Summoner(rsp.json())

	def get_summoner_by_name(self, name: str) -> Summoner:
		"""
			get summoner by their summoner name
		"""
		endpoint = f'{self.ep_summoner_by_name}{name}'
		rsp = self._api_call(self.platforms['NA1'], endpoint, {})
		return Summoner(rsp.json())

	def get_summoner_by_puuid(self, puuid: str) -> Summoner:
		"""
			gets summoner by their puuid
		"""
		endpoint = f'{self.ep_summoner_by_puuid}{puuid}'
		rsp = self._api_call(self.platforms['NA1'], endpoint, {})
		return Summoner(rsp.json())

	def get_summoner_by_summoner_id(self, summoner_id: str) -> Summoner:
		"""
			gets summoner by their summoner id
		"""
		endpoint = f'{self.ep_summoner_summonerid}{summoner_id}'
		rsp = self._api_call(self.platforms['NA1'], endpoint, {})
		return Summoner(rsp.json())

if __name__ == '__main__':
	from pprint import pprint
	sapi = SummonerAPI()
	summ = sapi.get_summoner_by_name('PoBeaver')
	print(summ.accountId())
	from judicator.api.leagueAPI import LeagueAPI
	lapi = LeagueAPI()
	entries = lapi.get_entries_by_summoner_id(summ.summonerId())
	pprint(entries)
	# print(sapi.get_summoner_by_account_id(summ.accountId()))
	# print(sapi.get_summoner_by_summoner_id(summ.summonerId()))
	# print(sapi.get_summoner_by_puuid(summ.puuid()))
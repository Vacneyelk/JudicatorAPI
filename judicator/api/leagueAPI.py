
from judicator.api.base import BaseAPI
from judicator.league import League

class LeagueAPI(BaseAPI):
	def __init__(self):
		BaseAPI.__init__(self)
		self.ep_entries_by_summoner_id = '/lol/league/v4/entries/by-summoner/'

	def get_entries_by_summoner_id(self, summoner_id: str):
		endpoint = f"{self.ep_entries_by_summoner_id}{summoner_id}"
		rsp = self._api_call(self.platforms['NA1'], endpoint, {})
		return [League(entry) for entry in rsp.json()]




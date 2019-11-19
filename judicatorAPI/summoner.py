import endpoints as ep
import credentials

from api_util import get_request

_API_PARAM = {
	'api_key' : credentials.API_KEY
}

class Summoner:
	def __init__(self, data: dict):
		self._data = data

	def profile_icon_id(self) -> int:
		""" returns profile icon id as an int """
		return self._data['profileIconId']

	def name(self) -> str:
		""" gets username of summoner """
		return self._data['name']

	def puuid(self) -> str:
		""" gets puuid of summoner """
		return self._data['puuid']

	def summoner_level(self) -> int:
		""" returns summoner level for summoner """
		return self._data['summonerLevel']

	def revision_date(self) -> int:
		""" returns last modified epoch of summoner """
		return self._data['revisionDate']

	def id(self) -> str:
		""" returns summoner id (max 63 characters) """
		return self._data['id']

	def account_id(self) -> str:
		""" returns account id (max 56 characters) """
		return self._data['accountId']

	def __str__(self):
		return f"Summoner: {self._data['name']} ({self._data['puuid']})"

def get_summoner_by_account_id(account_id: str):
	assert isinstance(account_id, str)
	rsp = get_request(
			f'https://{ep.EP_NA}{ep.EP_SUMMONER_ACCOUNT_ID}{account_id}', 
			params=_API_PARAM
		)
	return Summoner(rsp.json())

def get_summoner_by_name(name: str):
	assert isinstance(name, str)
	rsp = get_request(
			f'https://{ep.EP_NA}{ep.EP_SUMMONER_NAME}{name}', 
			params=_API_PARAM
		)
	return Summoner(rsp.json())

def get_summoner_by_puuid(puuid: str):
	assert isinstance(puuid, str)
	rsp = get_request(
			f'https://{ep.EP_NA}{ep.EP_SUMMONER_PUUID}{puuid}', 
			params=_API_PARAM
		)
	return Summoner(rsp.json())

def get_summoner_by_id(summoner_id: str):
	assert isinstance(summoner_id, str)
	rsp = get_request(
			f'https://{ep.EP_NA}{ep.EP_SUMMONER_SUMMONER_ID}{summoner_id}', 
			params=_API_PARAM
		)
	return Summoner(rsp.json())

# MAIN

if __name__ == '__main__':
	pass
	# TODO make a base class for inherit methods like code checks and other things
	# params = {
	#     'api_key' : credentials.API_KEY
	# }

	# rsp = requests.get(f'https://{ep.EP_NA}{ep.EP_SUMMONER_NAME}ApatheticLamp', params=params)
	# print(type(rsp))
	# print(rsp, rsp.url)
	# print(rsp.json())
	s = get_summoner_by_name('PoBeaver')
	# print(s.account_id())
	print(s.id())
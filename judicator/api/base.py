
from judicator.ratelimit.ratelimit import RateLimiter
from requests.models import Response
from judicator.config import API_KEY

import requests


class BaseAPI(RateLimiter):
	def __init__(self):
		RateLimiter.__init__(self)
		self.platforms = {
			'NA1' : 'na1.api.riotgames.com'
		}
		self.api_key = API_KEY

	def __check_response_code(self, rsp: Response):
		"""
			Used for checking response code and handling things
		"""
		# TODO: add real code checking
		if rsp.status_code != 200 or rsp.status_code != 429:
			rsp.raise_for_status()

	def _api_call(self, platform: str, endpoint: str, parameters: dict) -> Response:
		"""
			Send a request to the platform endpoint with the specified parameters
			This function also checks response codes and ratelimits in accordance to Riot's API rate limiting
			**WARNING**: This will cause your program to "sleep," check ratelimiting source for further understanding

			Args:
				platform: regional endpoint
				endpoint: specific api endpoint
				parameters: any parameters required for the api call

			Return:
				returns the response object for the api call
		"""
		# TODO: add custom exception in the case "api_key" already exists (it shouldnt)
		parameters['api_key'] = self.api_key
		url = f'https://{platform}{endpoint}'
		rsp = requests.get(url, params=parameters)
		self.__check_response_code(rsp)
		self._rate_limit(rsp)
		return rsp

if __name__ == '__main__':
	print('Running base.py')

	e = f'/lol/summoner/v4/summoners/by-name/ApatheticLamp'

	a = BaseAPI()
	rsp = a._api_call(a.platforms['NA1'], e, {})
	print(rsp.json())
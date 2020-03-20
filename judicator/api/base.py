
from judicator.ratelimit.ratelimit import RateLimiter
from requests.models import Response
from judicator.config import API_KEY

import requests

from time import sleep

from requests import RequestException
from requests.adapters import HTTPAdapter


# These error codes might be useless, I'll leave them here for now
# CURRENTLY NOT USED
class APIRequestError(RequestException):
	def __init__(self, *args, **kwargs):
		RequestException.__init__(self, *args, **kwargs)

class APIUnathorizedError(RequestException):
	def __init__(self, *args, **kwargs):
		RequestException.__init__(self, *args, **kwargs)

class APIForbiddenError(RequestException):
	def __init__(self, *args, **kwargs):
		RequestException.__init__(self, *args, **kwargs)

class APINotFoundError(RequestException):
	def __init__(self, *args, **kwargs):
		# RequestException.__init__(self, *args, **kwargs)
		super(APINotFoundError, self).__init__(*args, **kwargs)

class APIMethodError(RequestException):
	def __init__(self, *args, **kwargs):
		RequestException.__init__(self, *args, **kwargs)

class APITypeError(RequestException):
	def __init__(self, *args, **kwargs):
		RequestException.__init__(self, *args, **kwargs)

class APIRateLimitError(RequestException):
	def __init__(self, *args, **kwargs):
		RequestException.__init__(self, *args, **kwargs)

class APIResponseError(RequestException):
	def __init__(self, *args, **kwargs):
		RequestException.__init__(self, *args, **kwargs)

_ERROR_CODES = {
	400 : APIRequestError,
	401 : APIUnathorizedError,
	403 : APIForbiddenError,
	404 : APINotFoundError,
	405 : APIMethodError,
	415 : APITypeError,
	429 : APIRateLimitError,
	500 : APIResponseError,
	502 : APIResponseError,
	503 : APIResponseError,
	504 : APIResponseError
}


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
		if rsp.status_code != 200 and rsp.status_code != 429:
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

		# TODO: this needs to be reworked into a better solution, requests.Session retries potential solution
		# backoff implementation algo https://urllib3.readthedocs.io/en/latest/reference/urllib3.util.html#module-urllib3.util.retry
		backoff = 1.0
		max_retries = 5
		retries = 1
		while True:
			rsp = requests.get(url, params=parameters)
			self.__check_response_code(rsp)
			if int(rsp.status_code) < 500:
				break
			else:
				sleep( backoff * (2 ** (retries - 1)) )
				retries += 1
			if retries > max_retries:
				rsp.raise_for_status()

		self._rate_limit(rsp)
		return rsp

if __name__ == '__main__':
	print('Running base.py')

	e = f'/lol/summoner/v4/summoners/by-name/Apatheticlamp'

	a = BaseAPI()
	rsp = a._api_call(a.platforms['NA1'], e, {})
	print(rsp.json())
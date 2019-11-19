import time
import requests
from requests.models import Response

_CODES = {
    400 : 'bad request',
    401 : 'unauthorized',
    403 : 'forbidden',
    404 : 'not found',
    415 : 'unsupported media type',
    429 : 'rate limit exceeded',
    500 : 'internal server error',
    503 : 'service unavailable',
}

class UnexpectedResponseCode(Exception):
    def __init__(self, url: str = None, message: str = None):
        Exception.__init__(self, f'{url} - {message}')

def _reset_limit(rsp):
    """ 
        Sleeps the program for a certain amount of time

        This function should be called in the event the limit is exceeded for some reason
    """
    time.sleep(rsp.headers["Retry-After"])

def check_response_code(rsp: Response):
    """
        Checks the response code at takes appropriate action

        If the rate limit is exceeded the program will sleep in regard to the header

        If a bad status is found besides 429 an HTTPError will be raised

        Args
            rsp: response object from the requests module

        Return
            None

        Raises
            requests.exceptions.HTTPError
            UnexpectedResponseCode
    """
    if rsp.status_code == requests.codes.ok:
        return
    else:
        if rsp.status_code in _CODES:
            if rsp.status_code == 429:
                _reset_limit(rsp)
            else:
                rsp.raise_for_status()
        else:
            raise UnexpectedResponseCode(rsp.url, rps.status_code)

def _get_sleep_ratio(ratios: list, threshhold: float=0.95) -> float:
    """
        Calculates how long to sleep for an api call to safely rate limit api calls

        Args
            ratios: list of ratios, ratios = (sleep ratio, count ratio)
                sleep ratio = (seconds / calls)
                count ratio = (calls / max calls)
            threshhold: forces counts above this threshhold

        Return
    """
    force_idx = [idx for idx, r in enumerate(ratios) if r[1] > threshhold]

    if force_idx:
        # TODO: pick best sleep ratio
        return ratios[-1]
    else:
        return ratios[0]

def rate_limit(rsp: Response, debug: bool=False):
    """
        sleeps for a safe amount of time to respect riot rate limits

        Args:
            rsp:
    """

    def helper(x, y):
        """ returns (sleep ratio, count ratio) """
        l = x.split(':')
        c = y.split(':')
        return (float(l[1]) / float(l[0]) , float(c[0]) / float(l[0]))

    app_rate_limit = rsp.headers['X-App-Rate-Limit'].split(',')
    method_rate_limit = rsp.headers['X-Method-Rate-Limit'].split(',')

    app_rate_count = rsp.headers['X-App-Rate-Limit-Count'].split(',')
    method_rate_count = rsp.headers['X-Method-Rate-Limit-Count'].split(',')

    app_ratios = [helper(app_rate_limit[idx], app_rate_count[idx]) for idx in range(len(app_rate_limit))]

    method_ratios = [helper(method_rate_limit[idx], method_rate_count[idx]) for idx in range(len(method_rate_limit))]

    

    safe_app_ratio = _get_sleep_ratio(app_ratios)
    safe_method_ratio = _get_sleep_ratio(method_ratios)

    if debug:
        print('App ratios:', app_ratios)
        print('Metho ratios:', method_ratios)
        print('Safe app:', safe_app_ratio)
        print('Safe method:', safe_method_ratio)

    if safe_app_ratio[1] > 0.90:
        if debug: print('Sleeping for:', safe_app_ratio[0])
        time.sleep(safe_app_ratio[0])

    if safe_app_ratio > safe_method_ratio:
        if debug: print('Sleeping for:', safe_app_ratio[0])
        time.sleep(safe_app_ratio[0])
    else:
        if debug: print('Sleeping for:', safe_method_ratio[0])
        time.sleep(safe_method_ratio[0])

def get_request(url, params) -> Response:
    """
        Sends a get request, checks the codes, and sleeps in accordance with riot api rate limiting

        Args
            url: url to get
            params: params to pass with get

        Raises
            TODO: do exception processing

        Return
            Response object from requests.models.Reponse
    """
    rsp = requests.get(url, params=params)
    check_response_code(rsp)
    rate_limit(rsp)

    return rsp

if __name__ == '__main__':
    pass
    rsp = requests.get('https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/ApatheticLamp?api_key=RGAPI-ebcd5d57-9ba2-4ae1-9070-6c9e5ef3261f')
    from pprint import pprint
    # pprint(dict(rsp.headers))
    # app_rate = rsp.headers['X-App-Rate-Limit'].split(',')
    # print(app_rate)
    # ratio = lambda x: float(x[1]) / float(x[0])
    # for item in app_rate:
    #     print(ratio(item.split(':')))
    pprint(dict(rsp.headers))
    start = time.time()
    print(rate_limit(rsp, True))
    end = time.time()
    print('Elapsed:', end - start)


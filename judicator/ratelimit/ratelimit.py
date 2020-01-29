


from requests.models import Response
from time import time

class RateLimiter:
    def __init__(self):
        print('Init RateLimiter')

    def rate_limit(rsp: Response) -> None:
        """
            When passed a response object from the riot api we sleep the application for a safe amount of time based on the headers provided by the response. For more information go to https://developer.riotgames.com/docs/portal#web-apis_rate-limiting

            Args:
                rsp: response object from league of legends api

            Returns:
                None
        """
        if rsp.status_code == 429:
            self._reset_limit(rsp)
        
        def helper(x, y):
            """ returns (sleep ratio, count ratio) """
            l = x.split(':')
            c = y.split(':')
            return (float(l[1]) / float(l[0]), float(c[0]) / float(l[0]))

        app_rate_limit = rsp.headers['X-App-Rate-Limit'].split(',')
        method_rate_limit = rsp.headers['X-Method-Rate-Limit'].split(',')

        app_rate_count = rsp.headers['X-App-Rate-Limit-Count'].split(',')
        method_rate_count = rsp.headers['X-Method-Rate-Limit-Count'].split(',')

        app_ratios = [helper(app_rate_limit[idx], app_rate_count[idx]) for idx in range(len(app_rate_limit))]
        method_ratios = [helper(method_rate_limit[idx], method_rate_count[idx]) for idx in range(len(method_rate_limit))]

        safe_app_ratio = self._get_sleep_ratio(app_ratios)
        safe_method_ratio = self._get_sleep_ratio(method_ratios)

        if safe_app_ratio > safe_method_ratio:
            time.sleep(safe_app_ratio[0])
        else:
            time.sleep(safe_method_ratio[0])

    def _get_sleep_ratio(ratios: list, threshhold: float=0.95) -> float:
        """
            Calculates how long to sleep for an api call to safely rate limit api calls

            Args:
                ratios: list of ratios to sleep for various call rates
                threshhold: if a ratio is above this threshhold we want to prioritize it
            
            Returns:
                Float
        """
        force_idx = [idx for idx, r in enumerate(ratios) if r[1] > threshhold]

        if force_idx:
            # TODO: create hueristics for picking the best ratio to sleep for
            # I think current logic is if ratio is above threshhold prioritize later call ratios
            # otherwise we just sleep based on first call ratio
            return ratios[-1]
        else:
            return ratios[0]

    def _reset_limit(rsp: Response) -> None:
        """
            In the event a 429 error occurs we want to force a sleep until api calls are unlocked. This should never happen. This happens when a call exceeded the rate limit allowed.

            Args:
                rsp: response object from the riot api

            Returns:
                None
        """
        time.sleep(rsp.headers['Retry-After'])
        import sys
        print("429 Error, revisit rate limiting", file=sys.stderr)

# Judicator API

This is an API wrapper for the league of legends API. The purpose of this wrapper is to provide higher level access to the league of legends API for the Judicator project.

The Judicator API is not meant to be a full wrapper and does not cover all portions of the API. Only parts of the API that are deemed relevant to the Judicator project will have wrapper API access. If future portions of the API are deemed necessary then the wrapper will be extended.

If you wish to add to the project feel free to either fork and make your own developments or submit a pull request and it will be reviewed when I have time. Test cases should be provided or the likelihood of a pull request being accept is low due to a lack of time.

## Usage

A credentials module `credentials.py` should be created. A single variable should be included `API_KEY` that is assigned your API key as a string.

**NOTE:** Various information is encrypted with your API key. If you are using a development key you should check to find out if this is an issue for your use case. If it proves to be an issue you request a production key from the [Riot Developer Portal](https://developer.riotgames.com/apis#league-v4).

## Endpoints

Various endpoint values are provided in the `endpoints.py` module. All endpoints should begin with `EP_` with a descriptive name. Endpoints should be sectioned and grouped together.

## Development of modules

### API requests 

API requests should be performed with the `api_util.py` module

```python
from api_utils import get_request
# an alternative being
# import api_utils
import credentials

parameters = {
	'api_key' : credentials.API_KEY
}

def my_request():
	# make sure to pass a modified dictionary if your endpoint uses more parameters in the url
	# new_parameters = parameters.copy()
	# new_parameters['my param'] = 'value'
	
	rsp = get_request('url enpoint', params=parameter)
```

The `get_request` functional will handle rate limiting your requests for you. Please be aware this function will call `time.sleep(x)` and sleep the call for a safe amount of time based on the request headers from the league of legends API. This abstracts away the need to rate limit your calls and keeps your API key safe from 429 errors which will fail your API call and in the case of potentially damaging 429 calls, keep your key from getting banned.

Judicator was designed for automated use so this functionality was created with this in mind.

### What to do with responses

Responses to requests should be developed into a class for the response. This class should provide high level access to the response data as well as contain the response data so if necessary direct access can be done despite not encouraged for use.

### Documentation

All modules should have adequate type annontations along with docstrings. [Google has an excellent style guide for this.](http://google.github.io/styleguide/pyguide.html)

## Future development

Judicator API will add additional functionality as needed. Breaking changes might happen. This API wrapper was specifically developed with the Judicator project in mind and not to be a comprehensive fully fledged API wrapper. The wrapper comes as is and future developments are not promised.

TODO List

* Implement logging functionality across the API inorder to debug and provide contextual information during automated use to detect and hopefully fix unintended behavior.

import requests
import json

from api_poller.exceptions import APIRequestException


class APIRequestSession:
    def __init__(self, headers: dict[str, str] = {}):
        self._session = requests.session()
        self._session.headers = headers
    
    def _get_response(self, url:str, params:dict={}) -> requests.Response:
        response = self._session.get(url, params=params)
        if response.status_code == 200:
            return response
        else:
            raise APIRequestException(f"Received status code {response}")
    
    def get_json_response(self, url:str, params:dict={}) -> dict:
        """Retrieve json response as dict by sending a GET Request"""
        response = self._get_response(url, params=params)
        try:
            return response.json()
        except json.decoder.JSONDecodeError:
            print(response.text)
            raise APIRequestException(f"Expected json response")
    
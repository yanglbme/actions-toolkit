import os
from urllib.parse import quote

import requests


class OidcClient:

    @staticmethod
    def get_request_token() -> str:
        token = os.getenv('ACTIONS_ID_TOKEN_REQUEST_TOKEN')
        if not token:
            raise Exception('Unable to get ACTIONS_ID_TOKEN_REQUEST_TOKEN env variable')
        return token

    @staticmethod
    def get_id_token_url() -> str:
        runtime_url = os.getenv('ACTIONS_ID_TOKEN_REQUEST_URL')
        if not runtime_url:
            raise Exception('Unable to get ACTIONS_ID_TOKEN_REQUEST_URL env variable')
        return runtime_url

    @staticmethod
    def get_call(id_token_url: str):
        headers = {
            'Authorization': 'Bearer ' + OidcClient.get_request_token()
        }
        resp = requests.get(id_token_url, headers=headers)
        if resp.status_code != 200:
            raise Exception(f'Failed to get ID Token. \n'
                            f'Error Code: {resp.status_code}\n'
                            f'Result: {resp.text}')
        res = resp.json()
        if not res.get('value'):
            raise Exception('Response json body do not have ID Token field')
        return res['value']

    @staticmethod
    def get_id_token(audience: str = None):
        try:
            # New ID Token is requested from action service
            id_token_url = OidcClient.get_id_token_url()
            if audience:
                encoded_audience = quote(audience)
                id_token_url = f'{id_token_url}&audience={encoded_audience}'

            id_token = OidcClient.get_call(id_token_url)
            return id_token
        except Exception as e:
            raise Exception(f'Error message: {str(e)}')

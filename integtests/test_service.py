import requests
import os

def test_200_response():
    # apigw has o/p URL which should be written as environ-var=SERVICE_URL
    with requests.get(os.environ['SERVICE_URL']) as response:
        assert response.status_code == 300
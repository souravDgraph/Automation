import requests
from robot.api import logger

__all__ = ['RequestHandler']
__author__ = "Krishna Kaushik"
__version__ = "1.0"
__maintainer__ = "Krishna Kaushik"
__email__ = "tkrishnakaushik96@gmail.com"
__status__ = "Stagging"


# api = TestRailAPI("https://dgraph.testrail.io/", "tester@dgraph.io", "dgraph")

# api = TestRailAPI("https://dgraph.testrail.io/", "vivetha@dgraph.io", "Vera@5464")

class RequestHandler:

    def __init__(self, url):
        self.url = url

        self.headers = {}

    def post_request(self, appender, body):
        logger.info("Hitting post request at: "+self.url+appender)
        if appender == "/admin":
            self.headers = {
                'Content-Type': 'application/json'
            }
            response = requests.request("POST", self.url+appender, headers=self.headers, data=body)
        elif appender == "/admin/backup":
            response = requests.request("POST", self.url + appender, headers=self.headers, data=body)
        return response

    def get_request(self):
        response = requests.get(self.url)
        print(response.text)
        return response

    def get_request(self, appender):
        print("Hitting get request at: " + self.url+appender)
        response = requests.get(self.url+appender)
        print(response.text)
        return response

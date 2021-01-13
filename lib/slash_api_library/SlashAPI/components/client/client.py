#!\\usr\\bin\\env python

from robot.api import logger
from RequestsClient import RequestsClient
# pylint: disable=too-many-arguments, too-many-locals

__all__ = ['Connection']
__author__ = "Vivetha Madesh"
__copyright__ = "Copyright 2021, Dgraph.io"
__license__ = "DELL EMC"
__version__ = "1.0"
__maintainer__ = "Vivetha Madesh"
__email__ = "vivetha@dgraph.io"
__status__ = "Production"


class Connection(RequestsClient):
    """
    Connection Keywords
    """

    def __init__(self, *args, **kwargs):
        super(Connection, self).__init__(**kwargs)

    def create_session(self,
                       session_alias,
                       url,
                       headers,
                       timeout=300):

        return super(Connection, self).create_session(alias=session_alias,
                                url=url,
                                headers=headers)

    def delete_all_session(self):

        """ Deletes all vproxy RESTAPI sessions
        Returns None

        """
        _session = RequestsClient()
        _session.delete_all_sessions()

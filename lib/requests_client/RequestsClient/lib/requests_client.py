import logging

from RequestsLibrary import RequestsLibrary

__all__ = ['RequestsClient']


class RequestsClient(RequestsLibrary):
    """

    """

    def __init__(self, *args, **kwargs):
        super(RequestsClient, self).__init__(**kwargs)

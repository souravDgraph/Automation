# !/usr/bin/env python
# coding=utf-8
# pylint: disable=too-many-arguments
"""
Author: vivetha@dgraph.io
"""

from robot.api import logger
from jinja2 import Template
import json, os


__all__ = ['Utills']
__author__ = "Vivetha Madesh"
__version__ = "1.0"
__maintainer__ = "Vivetha Madesh"
__email__ = "vivetha@dgraph.io"
__status__ = "Production"


class Utills():
    """

    """

    @staticmethod
    def render_data_from_template(template_file,
                                  properties):
        template = Template(template_file)
        value = template.render(properties=properties)
        data = json.loads(value)
        return data

    @staticmethod
    def compare_dict_based_on_primary_dict_keys(primary_dict, secondary_dict):

        logger.info("comparing the primary and secondary Dicts")
        status = True
        for key in primary_dict.keys():
            logger.info("--.--." * 40)
            logger.info("primary dict - %s : %s " % (key, primary_dict[key]))
            logger.info("secondary dict - %s : %s " % (key, secondary_dict[key]))
            if primary_dict[key] != secondary_dict[key]:
                status = False
                logger.info("Expected data dint match")
        if not status:
            raise Exception("Expected data not found !!!")
            
    @staticmethod
    def render_template_path(template_file_name):
        template = None
        for root, dirs, files in os.walk("/"):
            for name in files:
                if name == template_file_name:
                    template = os.path.abspath(os.path.join(root, name))
        return template

    @staticmethod
    def render_template_path(template_file_name):
        template = None
        for root, dirs, files in os.walk("/"):
            for name in files:
                if name == template_file_name:
                    template = os.path.abspath(os.path.join(root, name))
        return template



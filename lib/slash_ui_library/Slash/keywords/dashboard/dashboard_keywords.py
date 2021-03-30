# !/usr/bin/env python
# coding=utf-8
# pylint: disable=too-many-arguments, missing-function-docstring
"""
Author: vivetha@dgraph.io
"""

from robot.api.deco import keyword
from Slash.keywords.browser.browser_keywords import BrowserKeywords
from Slash.locators.dashboard.dashboard import DashboardLocators


__all__ = ['DashboardKeywords']
__author__ = "Vivetha Madesh"
__version__ = "1.0"
__maintainer__ = "Vivetha Madesh"
__email__ = "vivetha@dgraph.io"
__status__ = "Production"


class DashboardKeywords():
    """Dashboard/Landing Page Keyword Library.

    Main operations:

    - create Backend.
    """
    timeout = 10
    @staticmethod
    def click_launch_new_backend(browser_alias):
        """
        click the launch new backend button.
        | browser_alias |  alias of the browser |

        Example:
        | Click Launch New Backend | browser_1 |

        Return:
            None
        """
        browser = BrowserKeywords.switch_browser(browser_alias)
        browser.click_element(DashboardLocators.create_backend, timeout=DashboardKeywords.timeout)
        browser.wait_until_page_contains_element(DashboardLocators.launch_new_backend_label, timeout=DashboardKeywords.timeout)

    @staticmethod
    def fill_backend_details(browser_alias,
                             backend_name,
                             select_product="Starter",
                             subdomain=None,
                             organization=None,
                             provider=None,
                             zone=None):
        """
        fill the backend details.
        | browser_alias |  alias of the browser |
        | backend_name |  name of the backend |
        | select_product |  product type for the backend |
        | subdomain |  subdomain for the backend |
        | organization |  organization for the backend |
        | provider |  provider for the backend |
        | zone |  zone for the backend |
        
        Example:
        | Fill Backend Details | browser_1 | test | 

        Return:
            None
        """
        browser = BrowserKeywords.switch_browser(browser_alias)
        browser.input_text(DashboardLocators.backend_name,
                           backend_name,
                           timeout=DashboardKeywords.timeout)
        if subdomain:
            browser.input_text(DashboardLocators.subdomain,
                               subdomain,
                               timeout=DashboardKeywords.timeout)
        if organization:
            browser.click_element(DashboardLocators.organization_select,
                                  timeout=DashboardKeywords.timeout)
            browser.click_element(DashboardLocators.organization_name.replace("%s", organization),
                                  timeout=DashboardKeywords.timeout)
        if provider:
            browser.click_element(DashboardLocators.provider.replace("%s", provider),
                                  timeout=DashboardKeywords.timeout)
        
        if select_product:
            browser.click_element(DashboardLocators.select_product.replace("%s", select_product),
                                    timeout=DashboardKeywords.timeout)

        if zone:
            browser.click_element(DashboardLocators.zone.replace("%s", zone),
                                  timeout=DashboardKeywords.timeout)

    @staticmethod
    def click_launch_button(browser_alias):
        """
        click the launch button in the launch new backend page.
        | browser_alias |  alias of the browser |

        Example:
        | Click Launch Button | browser_1 |

        Return:
            None
        """
        browser = BrowserKeywords.switch_browser(browser_alias)
        browser.click_element(DashboardLocators.launch_button,
                              timeout=DashboardKeywords.timeout)

    @staticmethod
    def monitor_backend_creation(browser_alias,
                                 timeout):
        """
        monitor the backend creation spinning for the backend.
        | browser_alias |  alias of the browser |
        | timeout | 10 |

        Example:
        | Monitor Backend Creation | browser_1 | 10 |

        Return:
            None
        """
        browser = BrowserKeywords.switch_browser(browser_alias)
        browser.wait_until_page_contains_element(DashboardLocators.spinning_backend,
                                                 timeout=DashboardKeywords.timeout)
        browser.wait_until_page_contains_element(DashboardLocators.cluster_usage,
                                                         timeout=timeout)
                                                         
    @staticmethod
    @keyword
    def click_schema_in_menu(browser_alias):
        """
        click the schema for the backend.
        | browser_alias |  alias of the browser |

        Example:
        | Click Schema In Menu | browser_1 |

        Return:
            None
        """
        browser = BrowserKeywords.switch_browser(browser_alias)
        browser.click_element(DashboardLocators.schema,
                              timeout=DashboardKeywords.timeout)
        browser.wait_until_page_contains_element(DashboardLocators.schema_label)

    @staticmethod
    @keyword
    def click_lambdas_in_menu(browser_alias):
        """
        click the lambdas for the backend.
        | browser_alias |  alias of the browser |

        Example:
        | Click Lambdas In Menu | browser_1 |

        Return:
            None
        """
        browser = BrowserKeywords.switch_browser(browser_alias)
        browser.click_element(DashboardLocators.lambdas,
                              timeout=DashboardKeywords.timeout)
        browser.wait_until_page_contains_element(DashboardLocators.lambdas_label)

    @staticmethod
    @keyword
    def click_settings_in_menu(browser_alias):
        """
        click the settings for the backend.
        | browser_alias |  alias of the browser |

        Example:
        | Click Settings In Menu | browser_1 |

        Return:
            None
        """
        browser = BrowserKeywords.switch_browser(browser_alias)
        browser.click_element(DashboardLocators.settings,
                              timeout=DashboardKeywords.timeout)
        browser.wait_until_page_contains_element(DashboardLocators.settings_label)

    @staticmethod
    def click_api_explorer_in_menu(browser_alias):
        """
        click the api explorer for the backend.
        | browser_alias |  alias of the browser |

        Example:
        | Click Api Explorer In Menu | browser_1 |

        Return:
            None
        """
        browser = BrowserKeywords.switch_browser(browser_alias)
        browser.click_element(DashboardLocators.api_explorer,
                                timeout=DashboardKeywords.timeout)
        browser.wait_until_page_contains_element(DashboardLocators.api_explorer_label)

    @staticmethod
    def click_overview_in_menu(browser_alias):
        """
        click the overview for the backend.
        | browser_alias |  alias of the browser |

        Example:
        | Click Overview In Menu | browser_1 |

        Return:
            None
        """
        browser = BrowserKeywords.switch_browser(browser_alias)
        browser.click_element(DashboardLocators.overview,
                                timeout=DashboardKeywords.timeout)
        browser.wait_until_page_contains_element(DashboardLocators.cluster_usage,
                                                         timeout=DashboardKeywords.timeout)

    @staticmethod
    def view_graphql_endpoint(browser_alias, endpoint):
        """
        view the graphql endpoint for the backend.
        | browser_alias |  alias of the browser |
        | endpoint |  graphql endpoint for the backend |

        Example:
        | View Graphql Endpoint | browser_1 | stgdgraph.aws.stage.thegaas.com/graphql |

        Return:
            None
        """
        browser = BrowserKeywords.switch_browser(browser_alias)
        browser.element_should_be_visible(DashboardLocators.graphql_endpoint.replace("%s", endpoint))

    @staticmethod
    def click_documentation_in_menu(browser_alias):
        """
        click the documentation for the backend.
        | browser_alias |  alias of the browser |

        Example:
        | Click Documentation In Menu | browser_1 |

        Return:
            None
        """
        browser = BrowserKeywords.switch_browser(browser_alias)
        browser.click_element(DashboardLocators.documentation,
                                timeout=DashboardKeywords.timeout)

    @staticmethod
    def click_avatar(browser_alias):
        """
        click the avatar present at the top right corner for the backend.
        | browser_alias |  alias of the browser |

        Example:
        | Click Avartar | browser_1 |

        Return:
            None
        """
        browser = BrowserKeywords.switch_browser(browser_alias)
        browser.click_element(DashboardLocators.avatar_button,
                                timeout=DashboardKeywords.timeout)

    @staticmethod
    def click_logout_button(browser_alias):
        """
        click the logout button.
        | browser_alias |  alias of the browser |

        Example:
        | Click Logout Button | browser_1 |

        Return:
            None
        """
        browser = BrowserKeywords.switch_browser(browser_alias)
        browser.click_element(DashboardLocators.logout,
                                    timeout=DashboardKeywords.timeout)

    @staticmethod
    def check_starter_product_disabled(browser_alias):
        """
        check the starter product disabled for the backend.
        | browser_alias |  alias of the browser |

        Example:
        | Check Starter Product Disabled | browser_1 |

        Return:
            None
        """
        browser = BrowserKeywords.switch_browser(browser_alias)
        browser.element_should_be_disabled(DashboardLocators.starter_product_disabled)

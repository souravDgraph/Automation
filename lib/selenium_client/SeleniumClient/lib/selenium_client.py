import logging

from SeleniumLibrary import SeleniumLibrary
from SeleniumLibrary.keywords.waiting import WaitingKeywords
from SeleniumLibrary.keywords.element import ElementKeywords
from SeleniumLibrary.keywords.formelement import FormElementKeywords
from robot.api.deco import keyword

try:
    from robot.api import logger as log
except ImportError:
    log = logging.getLogger(__name__)


__all__ = ['SeleniumClient']


class SeleniumClient(SeleniumLibrary):
    """

    """

    def __init__(self, *args, **kwargs):
        super(SeleniumClient, self).__init__(**kwargs)
        self.wait_keyword_object = WaitingKeywords(self)
        self.element_keyword_object = ElementKeywords(self)
        self.form_element_keyword_object = FormElementKeywords(self)

    @keyword
    def click_element(self,
                      locator,
                      modifier=False,
                      action_chain=False,
                      timeout=None,
                      error=None,
                      limit=None):
        """Waits until the element ``locator`` appears on the current page.

        Fails if ``timeout`` expires before the element appears. See
        the `Timeouts` section for more information about using timeouts and
        their default value and the `Locating elements` section for details
        about the locator syntax.

        ``error`` can be used to override the default error message.

        The ``limit`` argument can used to define how many elements the
        page should contain. When ``limit`` is `None` (default) page can
        contain one or more elements. When limit is a number, page must
        contain same number of elements.

        Click the element identified by ``locator``.

        See the `Locating elements` section for details about the locator
        syntax.

        The ``modifier`` argument can be used to pass
        [https://seleniumhq.github.io/selenium/docs/api/py/webdriver/selenium.webdriver.common.keys.html#selenium.webdriver.common.keys.Keys|Selenium Keys]
        when clicking the element. The `+` can be used as a separator
        for different Selenium Keys. The `CTRL` is internally translated to
        the `CONTROL` key. The ``modifier`` is space and case insensitive, example
        "alt" and " aLt " are supported formats to
        [https://seleniumhq.github.io/selenium/docs/api/py/webdriver/selenium.webdriver.common.keys.html#selenium.webdriver.common.keys.Keys.ALT|ALT key]
        . If ``modifier`` does not match to Selenium Keys, keyword fails.

        If ``action_chain`` argument is true, see `Boolean arguments` for more
        details on how to set boolean argument, then keyword uses ActionChain
        based click instead of the <web_element>.click() function. If both
        ``action_chain`` and ``modifier`` are defined, the click will be
        performed using ``modifier`` and ``action_chain`` will be ignored.

        Example:
        | Click Element | id:button |                   | # Would click element without any modifiers.               |
        | Click Element | id:button | CTRL              | # Would click element with CTLR key pressed down.          |
        | Click Element | id:button | CTRL+ALT          | # Would click element with CTLR and ALT keys pressed down. |
        | Click Element | id:button | action_chain=True | # Clicks the button using an Selenium  ActionChains        |
        """

        self.wait_keyword_object.wait_until_page_contains_element(locator,
                                                                  timeout,
                                                                  error)
        self.element_keyword_object.click_element(locator,
                                                  modifier,
                                                  action_chain)

    @keyword
    def input_text(self,
                   locator,
                   text,
                   clear=True,
                   timeout=None,
                   error=None,
                   limit=None):
        """
        Waits until the element ``locator`` appears on the current page.

        Fails if ``timeout`` expires before the element appears. See
        the `Timeouts` section for more information about using timeouts and
        their default value and the `Locating elements` section for details
        about the locator syntax.

        ``error`` can be used to override the default error message.

        The ``limit`` argument can used to define how many elements the
        page should contain. When ``limit`` is `None` (default) page can
        contain one or more elements. When limit is a number, page must
        contain same number of elements.

        Types the given ``text`` into the text field identified by ``locator``.

        When ``clear`` is true, the input element is cleared before
        the text is typed into the element. When false, the previous text
        is not cleared from the element. Use `Input Password` if you
        do not want the given ``text`` to be logged.

        If [https://github.com/SeleniumHQ/selenium/wiki/Grid2|Selenium Grid]
        is used and the ``text`` argument points to a file in the file system,
        then this keyword prevents the Selenium to transfer the file to the
        Selenium Grid hub. Instead, this keyword will send the ``text`` string
        as is to the element. If a file should be transferred to the hub and
        upload should be performed, please use `Choose File` keyword.

        See the `Locating elements` section for details about the locator
        syntax. See the `Boolean arguments` section how Boolean values are
        handled.
        """

        self.wait_keyword_object.wait_until_page_contains_element(locator,
                                                                 timeout,
                                                                 error)
        self.form_element_keyword_object.input_text(locator,
                                                    text,
                                                    clear)

    @keyword
    def click_button(self,
                     locator,
                     modifier=False,
                     timeout=None,
                     error=None,
                     limit=None):
        """
        Waits until the element ``locator`` appears on the current page.

        Fails if ``timeout`` expires before the element appears. See
        the `Timeouts` section for more information about using timeouts and
        their default value and the `Locating elements` section for details
        about the locator syntax.

        ``error`` can be used to override the default error message.

        The ``limit`` argument can used to define how many elements the
        page should contain. When ``limit`` is `None` (default) page can
        contain one or more elements. When limit is a number, page must
        contain same number of elements.

        Clicks the button identified by ``locator``.

        See the `Locating elements` section for details about the locator
        syntax. When using the default locator strategy, buttons are
        searched using ``id``, ``name``, and ``value``.

        See the `Click Element` keyword for details about the
        ``modifier`` argument.
        """
        self.wait_keyword_object.wait_until_page_contains_element(locator,
                                                                  timeout,
                                                                  error)
        self.element_keyword_object.click_button(locator,
                                                 modifier)

    @keyword
    def click_link(self,
                   locator,
                   modifier=False,
                   timeout=None,
                   error=None,
                   limit=None):
        """
        Waits until the element ``locator`` appears on the current page.

        Fails if ``timeout`` expires before the element appears. See
        the `Timeouts` section for more information about using timeouts and
        their default value and the `Locating elements` section for details
        about the locator syntax.

        ``error`` can be used to override the default error message.

        The ``limit`` argument can used to define how many elements the
        page should contain. When ``limit`` is `None` (default) page can
        contain one or more elements. When limit is a number, page must
        contain same number of elements.

        Clicks a link identified by ``locator``.

        See the `Locating elements` section for details about the locator
        syntax. When using the default locator strategy, links are searched
        using ``id``, ``name``, ``href`` and the link text.

        See the `Click Element` keyword for details about the
        ``modifier`` argument.
        """
        self.wait_keyword_object.wait_until_page_contains_element(locator,
                                                                  timeout,
                                                                  error)
        self.element_keyword_object.click_button(locator,
                                                 modifier)

    @keyword
    def get_text(self,
                 locator,
                 timeout=None,
                 error=None,
                 limit=None):
        """
         Waits until the element ``locator`` appears on the current page.

         Fails if ``timeout`` expires before the element appears. See
         the `Timeouts` section for more information about using timeouts and
         their default value and the `Locating elements` section for details
         about the locator syntax.

         ``error`` can be used to override the default error message.

         The ``limit`` argument can used to define how many elements the
         page should contain. When ``limit`` is `None` (default) page can
         contain one or more elements. When limit is a number, page must
         contain same number of elements.

         Returns the text value of the element identified by ``locator``.

        See the `Locating elements` section for details about the locator
        syntax.
        """
        self.wait_keyword_object.wait_until_page_contains_element(locator,
                                                                  timeout,
                                                                  error,
                                                                  limit)
        return self.element_keyword_object.get_text(locator)

    @keyword
    def get_value(self,
                  locator,
                  timeout=None,
                  error=None,
                  limit=None):
        """
        Waits until the element ``locator`` appears on the current page.

        Fails if ``timeout`` expires before the element appears. See
        the `Timeouts` section for more information about using timeouts and
        their default value and the `Locating elements` section for details
        about the locator syntax.

        ``error`` can be used to override the default error message.

        The ``limit`` argument can used to define how many elements the
        page should contain. When ``limit`` is `None` (default) page can
        contain one or more elements. When limit is a number, page must
        contain same number of elements.

        Returns the value attribute of the element identified by ``locator``.

        See the `Locating elements` section for details about the locator
        syntax.
        """
        self.wait_keyword_object.wait_until_page_contains_element(locator,
                                                                  timeout,
                                                                  error,
                                                                  limit)
        return self.element_keyword_object.get_value(locator)

    @keyword
    def get_element_attribute(self,
                              locator,
                              attribute,
                              timeout=None,
                              error=None,
                              limit=None):
        """
        Waits until the element ``locator`` appears on the current page.

        Fails if ``timeout`` expires before the element appears. See
        the `Timeouts` section for more information about using timeouts and
        their default value and the `Locating elements` section for details
        about the locator syntax.

        ``error`` can be used to override the default error message.

        The ``limit`` argument can used to define how many elements the
        page should contain. When ``limit`` is `None` (default) page can
        contain one or more elements. When limit is a number, page must
        contain same number of elements.

        Returns the value of ``attribute`` from the element ``locator``.

        See the `Locating elements` section for details about the locator
        syntax.

        Example:
        | ${id}= | `Get Element Attribute` | css:h1 | id |

        Passing attribute name as part of the ``locator`` was removed
        in SeleniumLibrary 3.2. The explicit ``attribute`` argument
        should be used instead.
        """
        self.wait_keyword_object.wait_until_page_contains_element(locator,
                                                                  timeout,
                                                                  error,
                                                                  limit)
        return self.element_keyword_object.get_element_attribute(locator,
                                                                 attribute)











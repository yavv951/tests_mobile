import os

import allure
import pytest
from _pytest.nodes import Item
from _pytest.runner import CallInfo
from allure_commons._allure import StepContext
from selene.support._logging import wait_with

from selene.support.shared import browser
from appium import webdriver
from dotenv import load_dotenv
from datetime import date

import config
from utils import utils


@pytest.fixture(scope='session', autouse=True)
def load_env():
    """
    Load .env
    """
    load_dotenv()


@pytest.fixture(scope='function', autouse=True)
def driver_management(request):
    browser.config.timeout = config.settings.timeout
    browser.config._wait_decorator = wait_with(
        context=StepContext
    )
    with allure.step('set up app session'):
        browser.config.driver = webdriver.Remote(
            config.settings.remote_url, options=config.settings.driver_options
        )

    yield

    # given we want to save disk space
    # then we store screenshots and xml dumps only for failed tests
    if config.settings.run_on_browserstack and request.node.result_of_call.failed:
        '''
        request.node is an "item" because we use the default "function" scope
        '''
        utils.allure.attach.screenshot(name='Last screenshot')
        utils.allure.attach.screen_xml_dump()

    session_id = browser.driver.session_id

    allure.step('close app session')(browser.quit)()

    if config.settings.run_on_browserstack:
        utils.allure.attach.video_from_browserstack(session_id)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item: Item, call: CallInfo):  # noqa
    # execute all other hooks to obtain the report object
    outcome = yield
    result_of_ = outcome.get_result()

    # set a report attribute for each phase of a call, which can
    # be "setup", "call", "teardown"
    setattr(item, 'result_of_' + result_of_.when, result_of_)


@pytest.fixture(scope='function')
def app_android_brs():
    """
    Create driver
    """
    USER = os.getenv('LOGIN')
    KEY = os.getenv('KEY')
    APPIUM_BROWSERSTACK = os.getenv('APPIUM_BROWSERSTACK')

    desired_cap = {
        "app": "bs://c700ce60cf13ae8ed97705a55b8e022f13c5827c",
        "deviceName": "Google Pixel 3",
        "platformVersion": "9.0",
        "platformName": "android",
        "project": "Python project",
        "build": "browserstack-build-" + str(date.today()),
        'bstack:options': {
            "projectName": "Second Python project",
            "buildName": "browserstack-build-DEMO2",
            "sessionName": "BStack second_test"
        }
    }
    browser.config.driver = webdriver.Remote(
        command_executor=f"https://{USER}:{KEY}@hub-cloud.browserstack.com/wd/hub",
        desired_capabilities=desired_cap
    )
    browser.config.timeout = 4
    yield app_android_brs
    browser.quit()

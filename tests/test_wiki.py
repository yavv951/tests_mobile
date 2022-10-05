import allure
from allure_commons._allure import step
from appium.webdriver.common.appiumby import AppiumBy
from selene import have, be
from selene.support.shared import browser

from atach.attachment import add_video
from utils.model import app


@allure.tag('mobile')
@allure.title('Test search')
def test_wiki_browserstack():
    app.given_opened()
    with step('Type search'):
        browser.element((AppiumBy.ACCESSIBILITY_ID, 'Search Wikipedia')).click()
        browser.element((AppiumBy.ID, "org.wikipedia.alpha:id/search_src_text")).type('BrowserStack')
    with step('Verify content found'):
        browser.all((AppiumBy.ID, 'org.wikipedia.alpha:id/page_list_item_title'))\
            .should(have.size_greater_than(0))
    add_video(browser)


@allure.tag('mobile')
@allure.title('Test search')
def test_wiki_not_found_text():
    app.given_opened()
    with step('Type search'):
        browser.element((AppiumBy.ACCESSIBILITY_ID, 'Search Wikipedia')).click()
        browser.element((AppiumBy.ID, "org.wikipedia.alpha:id/search_src_text")).type("Software quality assurance")
    with step('Verify content found'):
        browser.all(
            (AppiumBy.ID, 'org.wikipedia.alpha:id/page_list_item_title')
        ).should(have.size_greater_than(0))
    add_video(browser)


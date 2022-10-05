from appium.webdriver.common.appiumby import AppiumBy
from selene import be
from selene.support.shared import browser


def given_opened():
    if browser.element((AppiumBy.ID, "fragment_onboarding_skip_button")).matching(be.visible):
        #browser.element('#fragment_onboarding_skip_button').tap()
        browser.element((AppiumBy.ID, "org.wikipedia.alpha:id/fragment_onboarding_skip_button")).click()

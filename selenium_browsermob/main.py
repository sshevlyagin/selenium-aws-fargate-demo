import contextlib
from browsermobproxy import Server
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
import argparse

from selenium_browsermob import settings

config = settings.Config


@contextlib.contextmanager
def browser_and_proxy():
    server = Server(config.BROWSERMOB_PATH)
    server.start()
    proxy = server.create_proxy()
    proxy.new_har(options={'captureContent': True})

    # Set up Chrome
    option = webdriver.ChromeOptions()
    option.add_argument('--proxy-server=%s' % proxy.proxy)

    prefs = {"profile.managed_default_content_settings.images": 2}
    option.add_experimental_option("prefs", prefs)
    option.add_argument('--headless')
    option.add_argument('--no-sandbox')
    option.add_argument('--disable-gpu')

    capabilities = DesiredCapabilities.CHROME.copy()
    capabilities['acceptSslCerts'] = True
    capabilities['acceptInsecureCerts'] = True

    path = config.CHROME_PATH
    browser = webdriver.Chrome(options=option,
                               desired_capabilities=capabilities,
                               executable_path=path)

    try:
        yield browser, proxy
    finally:
        browser.quit()
        server.stop()


def scan_and_block_har(proxy):
    all_requests_finished = False
    while all_requests_finished is False:
        all_requests_finished = True
        for e in proxy.har['log']['entries']:
            if 'explore_tabs' in e['request']['url']:
                if e['response']['status'] != 200 or e['response']['content'].get('text') is None:
                    all_requests_finished = False
    return


def demo():
    with browser_and_proxy() as (browser, proxy):
        browser.get('https://www.airbnb.com/s/Seattle--WA--United-States/homes')
        first_listing_page_1 = browser.find_element_by_xpath('//div[contains(@id,"listing")]')
        scan_and_block_har(proxy)
        print('First Listing Page 1: {}'.format(first_listing_page_1.text))
        page_2 = browser.find_element_by_xpath('//li[@data-id="page-2"]')
        page_2.click()
        scan_and_block_har(proxy)
        first_listing_page_2 = browser.find_element_by_xpath('//div[contains(@id,"listing")]')
        print('First Listing Page 2: {}'.format(first_listing_page_2.text))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('config', type=str, nargs='?', help='the config class')
    args = parser.parse_args()
    config = getattr(settings, args.config)

    demo()

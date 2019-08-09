from selenium import webdriver
import argparse

from selenium_simple import settings

config = settings.Config


def demo():
    option = webdriver.ChromeOptions()
    # Options based on Stack Overflow posts and https://developers.google.com/web/updates/2017/04/headless-chrome
    option.add_argument('--headless')
    option.add_argument('--no-sandbox')
    option.add_argument('--disable-gpu')

    browser = webdriver.Chrome(options=option, executable_path=config.CHROME_PATH)
    browser.get('http://www.xkcd.com')
    comic_element = browser.find_element_by_xpath('//div[@id="comic"]//img')
    comic_alt_txt = comic_element.get_attribute('title')
    print('The XKCD comic alt_text is "{}"'.format(comic_alt_txt))
    browser.quit()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('config', type=str, nargs='?', help='the config class')
    args = parser.parse_args()
    config = getattr(settings, args.config)

    demo()
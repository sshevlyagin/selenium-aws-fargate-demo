class Config(object):
    CHROME_PATH = '/Library/Application Support/Google/chromedriver76.0.3809.68'
    BROWSERMOB_PATH = '/usr/local/bin/browsermob-proxy-2.1.4/bin/browsermob-proxy'


class Docker(Config):
    CHROME_PATH = '/usr/local/bin/chromedriver'

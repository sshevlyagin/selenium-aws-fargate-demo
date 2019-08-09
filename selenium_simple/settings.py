class Config(object):
    CHROME_PATH = '/Library/Application Support/Google/chromedriver76.0.3809.68'


class Docker(Config):
    CHROME_PATH = '/usr/local/bin/chromedriver'

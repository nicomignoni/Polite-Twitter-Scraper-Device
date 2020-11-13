import pyautogui

#### CLASS SETTINGS ####
WEBDRIVER_PATH = 'C:\Program Files\Mozilla Firefox\geckodriver.exe'
SCROLL_PAUSE_TIME = 3  # secs
AUTO_SCROLLING = True
LANGUAGE = 'en'
TIME_STAMP_LIST_LIMIT = 200
SCREEN_LENGHT, WINDOW_HIGH = pyautogui.size()
LOGIN = False
EMAIL = 'nicola.mignoni@gmail.com'
JSON_FILE_NAME = 'news.json'
########################

#### SEARCH SETTINGS ####
SEARCH_LIMIT = 5000
## Words ##
ALL_OF_THESE_WORDS = ''
THIS_EXACT_PHRASE = ''
ANY_OF_THESE_WORDS = ''
NONE_OF_THESE_WORDS = ''
HASHTAGS = ()
## Account ##
FROM_THESE_ACCOUNTS = ''
TO_THESE_ACCOUNTS = ''
MENTIONING_THESE_ACCOUNTS = ''
## Filters ##
REPILES = True
INCLUDE_REPILES_AND_ORIGINAL_TWEETS = True
ONLY_SHOW_REPLIES = False
LINKS = False
INCLUDE_TWEETS_WITH_LINKS = False
ONLY_SHOW_TWEETS_WITH_LINKS = False
## Dates ##
FROM_DATE = '' #AAAA-MM-GG
TO_DATE = '' #AAAA-MM-GG

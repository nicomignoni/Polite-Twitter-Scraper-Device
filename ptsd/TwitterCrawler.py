from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from bs4 import BeautifulSoup
from datetime import datetime
import time, re, json, pyautogui, getpass, os
import settings as s

browser = webdriver.Firefox(executable_path=s.WEBDRIVER_PATH)
browser.set_window_size(s.SCREEN_LENGHT / 2, s.WINDOW_HIGH)
browser.set_window_position(0, 0)
browser.implicitly_wait(10)

hashtag_index = 0

class TwitterCrawler:
    def __init__(self):
        self.tweets_trail = dict()
        self.store_tweet_ETA = 0
        self.get_user_waiting_time = 0
        self.local_timestamps = []
        self.current_dict_size = None
        self.loaded_json = dict()
        self.search()
        
        if s.AUTO_SCROLLING:
            self.json_file_name = s.JSON_FILE_NAME
            if not os.path.exists(os.path.abspath(self.json_file_name)):
                with open(self.json_file_name, 'w') as f:
                    json.dump(dict(), f)
        else:
            self.json_file_name = 'twitter-session-{}-{}'.format(datetime.now().strftime("%d-%m-%YT%H.%M.%S"),
                                                                 s.HASHTAGS[hashtag_index] + '.json')
            with open(self.json_file_name, 'w') as f:
                json.dump(dict(), f)
        with open(self.json_file_name, 'r') as f:
            self.loaded_json = json.load(f)
        if self.loaded_json:
            self.old_timestamps = {(tweet['time'], tweet['user']) for tweet in self.loaded_json.values() if 'user' in tweet}
        else:
            self.old_timestamps = set()
        self.initial_dict_size = len(self.loaded_json)
        self.current_dict_size = len(self.loaded_json)
        print('Initial number in self.loaded_json: ', len(self.loaded_json))
                    
        if s.LOGIN:
            self.login()

    def login(self):
        login_button = browser.find_element_by_link_text('Log in')
        if login_button is not None:
            login_button.click()
            username_bar = browser.find_element_by_xpath("//input[@name='session[username_or_email]']")
            while True:
                password_bar = browser.find_element_by_xpath("//input[@name='session[password]']")
                username_bar.send_keys(s.EMAIL)
                password_bar.send_keys(getpass.getpass())
                browser.find_element_by_xpath("//div[@data-testid='LoginForm_Login_Button']").click()
                if 'error' not in browser.current_url:
                    break

    def search(self):
        url_search = 'https://twitter.com/search?lang=' + s.LANGUAGE + '&q=('
        if s.ALL_OF_THESE_WORDS:
            url_search = url_search + s.ALL_OF_THESE_WORDS.replace('', '%20')
        if s.THIS_EXACT_PHRASE:
            url_search = url_search + '%20%22' + s.THIS_EXACT_PHRASE.replace('', '%20') 
        if s.ANY_OF_THESE_WORDS:
            url_search = url_search + '%22%20(' + s.ANY_OF_THESE_WORDS.replace('', '%20OR%20') + ')'
        if s.NONE_OF_THESE_WORDS:
            url_search = url_search + '%20-' + s.NONE_OF_THESE_WORDS.replace('', '%20-')
        if s.HASHTAGS:
            if s.HASHTAGS[hashtag_index]:
                url_search = url_search + '%20(%23' + s.HASHTAGS[hashtag_index] + ')'
        if s.FROM_THESE_ACCOUNTS:
            url_search = url_search + '%20(from%3' + s.FROM_THESE_ACCOUNTS.replace('', '%20') + ')'
        if s.TO_THESE_ACCOUNTS:
            url_search = url_search + '%20(to%3' + s.TO_THESE_ACCOUNTS.replace('', '%20') + ')'
        if s.MENTIONING_THESE_ACCOUNTS:
            url_search = url_search + '%20(' + s.MENTIONING_THESE_ACCOUNTS.replace('', '%20') + ')'
        if not s.REPILES:
            url_search = url_search + '%20-filter%3Areplies'
        if not s.LINKS:
            url_search = url_search + '%20-filter%3Alinks'
        if s.FROM_DATE:
            url_search = url_search + '%20since%3A' + s.FROM_DATE
        if s.TO_DATE:
            url_search = url_search + '%20until%3A' + s.TO_DATE
        browser.get(url_search)
        
    def get_tweets(self):
        global hashtag_index
        k = 0
        dirty_tweets = browser.find_elements_by_xpath("//article")
        for dirty_tweet in dirty_tweets:
            try:
                parsed_tweet = BeautifulSoup(
                        f"<{dirty_tweet.tag_name}>{dirty_tweet.get_attribute('innerHTML')}</{dirty_tweet.tag_name}>",
                        features="lxml")
                user_tag = parsed_tweet.find('a')
                time_tag = parsed_tweet.find('time')
                text_tag = parsed_tweet.find('div', {'lang': s.LANGUAGE})
                if time_tag is not None and \
                        text_tag is not None and \
                        user_tag is not None:
                    timestamp = time_tag['datetime'][:-5]
                    user = user_tag['href'].replace('/', '')
                    text = text_tag.text.replace('\n', '')
                    if (timestamp, user) not in self.local_timestamps and \
                            (timestamp, user) not in self.old_timestamps:
                        current_date = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
                        k += 1
                        ID = self.current_dict_size + k
                        tweet = {ID: {
                            'read_at': current_date,
                            'time': timestamp,
                            'user': user,
                            'text': text,
                            'replies': 0,
                            'retweets': 0,
                            'likes': 0,
                            # 'hashtags': re.findall('#[A-Za-z]*\d*', text)
                            # 'mentions': re.findall('@[A-Za-z]*\d*', text)
                            }}
                        response = parsed_tweet.find('div', {"aria-label":
                                            re.compile('(.*replies?|reply?.*Retweets?|Retweet?.*likes?|like?)|'),
                                                                  "role": "group"})
                        if response is not None:
                            if 'replies' in response or 'reply' in response:
                                replies = re.search("(1 reply)|(\d* replies)", response).group()
                                tweet['replies'] = re.search('\d*', replies).group()
                            if 'Retweets' in response or 'Retweet' in response:
                                retweets = re.search("(1 Retweet)|(\d* Retweets)", response).group()
                                tweet['retweets'] = re.search('\d*', retweets).group()
                            if 'likes' in response or 'like' in response:
                                likes = re.search("(1 like)|(\d* likes)", response).group()
                                tweet['likes'] = re.search('\d*', likes).group()    
                        # print(tweet)
                        self.tweets_trail.update(tweet)
                        print('Tweets in trail:', len(self.tweets_trail), user)
                        self.local_timestamps.append((timestamp, user))
                        if len(self.local_timestamps) > s.TIME_STAMP_LIST_LIMIT:
                            del self.local_timestamps[0]
            except StaleElementReferenceException:
                pass

    def get_user(self, user):
        browser.get('https://twitter.com/'+ user)
        try:
            location_tag = browser.find_element_by_xpath("//*[local-name()='svg']/following-sibling::span/span")
        except NoSuchElementException:
            location = ''
        else:
            location = location_tag.text
        following = browser.find_element_by_xpath("//a[contains(@href, 'following')]").text
        followers = browser.find_element_by_xpath("//a[contains(@href, 'followers')]").text
        user_info = {user: {
            'location': location,
            'following': following,
            'followers': followers
            }}
        return user_info

    def store_tweet_trail(self):
        start_time = time.time()
        if self.tweets_trail:
            if not self.loaded_json:
                with open(self.json_file_name, 'r') as f:
                    self.loaded_json = json.load(f)
            self.loaded_json.update(self.tweets_trail)
            self.current_dict_size = len(self.loaded_json)
            print('Number of tweets in self.loaded_json.update: ', len(self.loaded_json))
            self.tweets_trail = dict()
            with open(self.json_file_name, 'w') as f:
                json.dump(self.loaded_json, f)
        end_time = time.time()
        self.store_tweet_ETA = end_time - start_time

    def scroll_and_scrape(self):
        global hashtag_index
        while True:
            last_height = browser.execute_script("return document.body.scrollHeight")
            if s.AUTO_SCROLLING:
                browser.execute_script("window.scrollBy(0, document.body.scrollHeight + 1000);")
            self.store_tweet_trail()
            if self.store_tweet_ETA < s.SCROLL_PAUSE_TIME and s.AUTO_SCROLLING:
                time.sleep(s.SCROLL_PAUSE_TIME - self.store_tweet_ETA)
            self.get_tweets()
            new_height = browser.execute_script("return document.body.scrollHeight")
            if new_height == last_height and s.AUTO_SCROLLING:
                pass
            if crawler.current_dict_size - crawler.initial_dict_size > s.SEARCH_LIMIT and s.AUTO_SCROLLING:
                if hashtag_index < len(s.HASHTAGS)-1:
                    hashtag_index += 1
                    crawler.__init__()
                else:
                    break

if __name__ == '__main__':
    crawler = TwitterCrawler()
    while True:
        crawler.scroll_and_scrape()
        
            
                
        
        

<h1 id="polite-twitter-scraper-device-ptsd">Polite Twitter Scraper Device (PTSD)</h1>
<h2 id="introduction">Introduction</h2>
<p>This application tries to provide a tool to politely scrape Twitter, using a browser-automation approach. Python’s Selenium has been used to automatize the process of collecting the tweets, loaded in the webpage, via HTML parsing. It is also possible to scrape the webpage while manually scrolling it, in order to record the tweets encountered during the navigation.</p>
<h2 id="requirements">Requirements</h2>
<p>In this  tool, Selenium uses Mozilla Firefox as browser. In order to function properly, you need to download the <a href="%5Bhttps://github.com/mozilla/geckodriver/releases%5D(https://github.com/mozilla/geckodriver/releases)">webdriver</a>.</p>
<blockquote>
<p>Although it is possible to use Selenium with other browser, PTSD has only been tested with Firefox.</p>
</blockquote>
<p>The following libraries are required. Please, check if you need to install any of them.</p>
<ul>
<li><a href="https://pypi.org/project/selenium/">Selenium</a></li>
<li><a href="https://pypi.org/project/beautifulsoup4/">BeautifulSoup</a></li>
<li><a href="https://pypi.org/project/PyAutoGUI/">pyautogui</a></li>
</ul>
<h2 id="settings">Settings</h2>
<p>The <code>settings.py</code> file contains the main setting parameters that should be adjusted before we start:</p>
<h3 id="general-settings">General Settings</h3>
<ul>
<li><code>WEBDRIVER_PATH</code> (<em>str</em>): the webdriver directory.</li>
<li><code>SCROLL_PAUSE_TIME</code> (<em>int</em>): the waiting time between one scroll and the other (in seconds). Default is 2 sec.</li>
<li><code>AUTO_SCROLLING</code> (<em>bool</em>): whether to active the auto-scroll mode.</li>
<li><code>LANGUAGE</code> (<em>str</em>): the language the tweets text. Default is <code>'en'</code>.</li>
<li><code>TIME_STAMP_LIST_LIMIT</code>  (<em>int</em>): the number of tweets stored in a log in order to avoid collecting the same tweet more than once while navigating. Default is 300.</li>
<li><code>LOGIN</code> (<em>bool</em>): whether to access your account while scraping. <em>(optional)</em>.</li>
<li><code>EMAIL</code> (<em>str</em>): account’s email <em>(optional)</em>.</li>
</ul>
<h3 id="search-settings">Search Settings</h3>
<ul>
<li><code>SEARCH_LIMIT</code> (<em>int</em>): the max number of tweets to retrive per hashtag. When the limit is reached, the next hashtag will be considered and a new search will begin.</li>
</ul>
<p>The following parameters mirror the Twitter <a href="https://twitter.com/search-advanced">advanced search</a> form.</p>

<table>
<thead>
<tr>
<th align="center"><strong>Words</strong></th>
<th align="center"><strong>Account</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td align="center"><code>ALL_OF_THESE_WORDS</code> (<em>str</em>)</td>
<td align="center"><code>FROM_THESE_ACCOUNTS</code> (<em>str</em>)</td>
</tr>
<tr>
<td align="center"><code>THIS_EXACT_PHRASE</code> (<em>str</em>)</td>
<td align="center"><code>TO_THESE_ACCOUNTS</code> (<em>str</em>)</td>
</tr>
<tr>
<td align="center"><code>ANY_OF_THESE_WORDS</code> (<em>str</em>)</td>
<td align="center"><code>MENTIONING_THESE_ACCOUNTS</code> (<em>str</em>)</td>
</tr>
<tr>
<td align="center"><code>NONE_OF_THESE_WORDS</code> (<em>str</em>)</td>
<td align="center"><strong>Filters</strong></td>
</tr>
<tr>
<td align="center"><code>HASHTAGS</code> (<em>list</em> or <em>tuple</em>)</td>
<td align="center"><code>REPILES</code> (<em>bool</em>)</td>
</tr>
<tr>
<td align="center"><strong>Date</strong></td>
<td align="center"><code>LINKS</code> (<em>bool</em>)</td>
</tr>
<tr>
<td align="center"><code>FROM_DATE</code> (<em>str</em>, ‘<em>yyyy-mm-dd</em>’)</td>
<td align="center"></td>
</tr>
<tr>
<td align="center"><code>TO_DATE</code> (<em>str</em>, ‘<em>yyyy-mm-dd</em>’)</td>
<td align="center"></td>
</tr>
</tbody>
</table><h2 id="minimal-documentation">Minimal documentation</h2>
<p>The <code>TwitterCrawler.py</code> launches Firefox and returns you the Twitter homepage. If  <code>AUTO_SCROLLING</code> is active, the webpage will be scrolled and scraped automatically. If not, tweets will be collected while you navigate.</p>
<p>You can also import the <code>TwitterCrawler.py</code> in your project and use the <code>TwitterCrawler()</code> class. Briefly:</p>
<ul>
<li><code>TwitterCrawler().login(email)</code>: allows Twitter login</li>
<li><code>TwitterCrawler().search()</code>: initializes a search based on the parameters previously defined</li>
<li><code>TwitterCrawler().get_tweets()</code>: collects the tweets present in the loaded page.</li>
<li><code>TwitterCrawler().get_user(user)</code>: redirects to /username page and returns a dict with followers, following and location (if present).</li>
<li><code>TwitterCrawler().scroll_and_scrape()</code>: initializes the scrolling process (if <code>AUTO_SCROLLING</code> is <code>True</code>). Otherwise, it stands by waiting for you to scroll.</li>
</ul>
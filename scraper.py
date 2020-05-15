from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from datetime import datetime
import requests, time, os, bs4, sys, re


class Scraper():
  def __init__(self, sub, num_of_posts):
    # define variables to call in other functions inside the class
    self.num_of_posts = num_of_posts
    self.sub = sub

    # driver options
    options = Options()
    #options.add_argument('--headless')
    options.add_argument('--disable-gpu')

    # open the driver
    self.driver = webdriver.Chrome(options=options)
    # go to the sub we want to scrape
    self.driver.get("https://www.reddit.com/r/" + sub + "/top/?t=day")
    # scroll down to load posts (depends on how many posts we want to download, needs to be int to work in while loop)
    n_pagedowns = round(self.num_of_posts * 1.5)
    while n_pagedowns:
      self.driver.find_elements_by_tag_name("body")[0].send_keys(Keys.PAGE_DOWN)
      time.sleep(1)
      n_pagedowns -= 1
      
    # define the sauce to use bs4 to scrape
    self.sauce = self.driver.page_source
    self.driver.quit()

  
  def get_data(self):
    # define soup to parse the sauce
    soup = bs4.BeautifulSoup(self.sauce, 'lxml')
    # find all the posts
    posts = soup.find_all("div", attrs={"class": "_1poyrkZ7g36PawDueRza-J"})
    # object which will hold title posts and images {title: image source}
    obj = {}
    # variable to establish the number of times we're gonna loop to get the data we need
    posts_to_download = 0

    # define loops we need to dowload posts we got/posts we want
    if (len(posts) < self.num_of_posts):
      posts_to_download = len(posts)
    elif (self.num_of_posts <= len(posts)):
      posts_to_download = self.num_of_posts + 1

    # get the post data depending on the media type
    for i in range(posts_to_download):
      title = posts[i].find('h3', attrs={'class': '_eYtD2XCVieq6emjKBH3m'}).text
      title = re.sub('[^A-Za-z0-9 ]+', '', title)
      src = ''

      if (len(posts[i].find_all('img', attrs={'class': 'ImageBox-image'})) == 1):
        src = posts[i].find('img', attrs={'class': 'ImageBox-image'})['src']
      elif (len(posts[i].find_all('source')) == 1):
        src = posts[i].find('source')['src']
      else: # missing condition to download videos contained in an iframe
        continue

      obj[title] = src
      
    return obj


  def download(self):
    # get the current date to create dir
    current_date = datetime.today().strftime("%Y-%m-%d")
    # create the path to the directory where imgs will be downloaded
    path = "media/" + self.sub + "/" + current_date + "/"

    # get the data (object containing titles and media srcs)
    data = self.get_data()

    if (data): # if we found posts with media, create dir and download
      # if path doesnt exist, create it
      if (not os.path.exists(path)):
        os.makedirs(path)

      # loop through object and download and save media
      for key in data:
        title = key
        src = data[key]
        
        # the method we download the media depends on the media type (supports imgs and gifs)
        if (".gif" in src):
          r = requests.get(src, stream=True)
          with open(path + "/" + title + ".mp4", "wb") as writer:
            for chunk in r.iter_content(chunk_size=1024*1024):
              if chunk:
                writer.write(chunk)
        elif (".jpeg" in src) or (".jpg" in src) or (".png" in src):
          img = requests.get(data[key])
          with open(path + "/" + title + ".jpg", "wb") as writer:
            writer.write(img.content)
        else:
          continue
        
        time.sleep(1)
    else: # we didn't find any media posts to download
      print("No posts with media were found, exiting.")
      return
      
  
sub = str(sys.argv[1])
num_of_posts = int(sys.argv[2])

scraper = Scraper(sub=sub, num_of_posts=num_of_posts)
scraper.download()

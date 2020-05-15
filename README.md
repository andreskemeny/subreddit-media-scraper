# subreddit-media-scraper

Download top N media posts of the day of any subreddit you want.

## Dependencies

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install Selenium, BeautifulSoup4 and requests.

```bash
pip install selenium
pip install bs4
pip install requests
```

and install and configure Chrome WebDriver.

## Usage

Go to project directory and run

```bash
python3 scraper.py <subreddit> <number of posts>
```

subreddit must be a string of the name of the subreddit you want to scrape, for example: dankmemes.    
number of posts must be an integer defining the number of media posts you want to download, for example: 10.

### Example

```bash
python3 scraper.py dankmemes 10
```

## Download Location
Media the scraper downloads will be saved at    

 
```
Project Directory    
├── media
    ├── <subreddit1>
        └── <date scraped>
            ├── <title of post1>
            └── <title of post2>
    ├── <subreddit2>
        └── <date scraped>
            ├── <title of post1>
            └── <title of post2>
    └── <subredditN>
        └── <date scraped>
            ├── <title of post1>
            └── <title of post2>
```

## Warning
The scraper works best for subreddits dedicated to uploading images, like r/EarthPorn, or meme subreddits like r/dankmemes.    

Script works by scrolling down looking for media; if no posts with media are found, none will be downloaded, if more than "number of posts" are found, only "number of posts" will be downloaded.
   
**Disclaimer: This script is intended for personal use and I am not liable for copyright infringement as a result of using this script.**

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)

![UYTS Banner](images/banner.png)
![GitHub Workflow Status](https://img.shields.io/github/workflow/status/w-henderson/Unlimited-YouTube-Search/UYTS-Tests) ![License](https://img.shields.io/github/license/w-henderson/unlimited-youtube-search) ![PyPI - Downloads](https://img.shields.io/pypi/dm/unlimited-youtube-search?color=green) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/unlimited-youtube-search) ![GitHub Repo stars](https://img.shields.io/github/stars/w-henderson/unlimited-youtube-search)

# Unlimited YouTube Search
Unlimited YouTube Search (UYTS) is a quick and easy way to search YouTube from your Python program without the need for the YouTube Data API. It's a Python port of [youtube-scrape](https://github.com/HermanFassett/youtube-scrape) by [Herman Fassett](https://github.com/HermanFassett) and has the majority of its features.

## How do I install it?
Simply run `pip install unlimited-youtube-search` in the command prompt to install it from the Python Package Index. Alternatively, clone the repo to your PC, navigate to its folder, and run `python setup.py install`. Both of these methods will install UYTS and its dependencies.

## How do I use it?
You'll need to import `uyts` at the start of your project in order to use Unlimited YouTube Search. From then on, you can search YouTube using `search = uyts.Search('search query')`. This returns a search object which has the attribute `results` storing a list of Video, Playlist and Channel objects. For example, you could run `print(search.results[0].title)` to see its title. For more information, read on.

## Simple Example Program
Here's a simple program to show how easy it is to search YouTube with UYTS.
```py
import uyts

query = input("Search query: ")
search = uyts.Search(query)

for result in search.results:
    print(result)
```

## What if I want to host a server with it?
That's already built in! To host a server, simply run the following code:
```py
from uyts import Server
app = Server()
app.run()
```
This will host a Flask server on port 80. More information on how to customise this is in the documentation below.

# Documentation

### Search class
Usage: `uyts.Search(query,minResults=0)`

Parameters:
- `query`: the string to search for
- `minResults` (optional): the minimum number of results to return. UYTS will continue making requests until it reaches this number or runs out of results. The default value of 0 will make one search request.

Attributes:
- `results`: list of search results
- `resultsJSON`: JSON object of search results
- `query`: the original search query
- `resultsCount`: the number of search results returned
- `maxResultsCount`: YouTube's estimation of total possible search results

The following three classes are returned in the search results, and while they can be created yourself, there's pretty much no reason you would want to do that so I haven't included how to do so here. It's self explanatory in the code however.

### Video class
Attributes:
- `id`: the ID of the YouTube video
- `title`: the title of the YouTube video
- `thumbnail_src`: the URL of the thumbnail
- `views`: the number of views
- `author`: the name of the uploader
- `duration`: the duration of the video
- `resultType`: the type of result (in this case, `video`)
- `ToJSON()`: returns the video as a JSON object
- `ToXML()`: returns the video as an XML string

### Playlist class
Attributes:
- `id`: the ID of the playlist
- `title`: the title of the playlist
- `thumbnail_src`: the URL of the thumbnail
- `length`: the number of videos in the playlist
- `author`: the name of the creator
- `resultType`: the type of result (in this case, `playlist`)
- `ToJSON()`: returns the playlist as a JSON object
- `ToXML()`: returns the playlist as an XML string

### Channel class
Attributes:
- `id`: the ID of the channel
- `title`: the name of the channel
- `subs` or `subscriber_count`: the number of subscribers the channel has
- `resultType`: the type of result (in this case, `channel`)
- `ToJSON()`: returns the channel as a JSON object
- `ToXML()`: returns the channel as an XML string

### Server class
The server must be initialised before you can call `run()`.

Parameters:
- `serverName` (optional): the name for the Flask server, defaults to `uyts-api`
- `serverMessage` (optional): the message that appears on the server homepage, defaults to `Server online`
- `rawHTML` (optional): if `True`, treats `serverMessage` as raw HTML rather than a string, defaults to `False`

Methods:
- `run(host="0.0.0.0",port=80)`: runs a Flask server on your local IP on port 80, unless specified otherwise

Attributes:
- `app`: this is a Flask object for the server. For most use-cases you won't need to directly interact with it. However, if you wanted to deploy this to Heroku you would need to do something like `server = uyts.Server().app` and then use Gunicorn to run it with `web: gunicorn main:server` for the Procfile as you can't run something from inside a class (e.g. `web: gunicorn main:server.app` would be invalid).

Server routes:
- `/`: main page, should show "Server online" if the server is online
- `/api`: API page, either GET `/api/<query>` or `/api/<query>/<minResults>` depending on whether you want to specify the minimum results. The response should look like this (but with more results):
```json
[
    {
        "id": "dQw4w9WgXcQ",
        "title": "Rick Astley - Never Gonna Give You Up (Video)",
        "thumbnail_src": "http://i.ytimg.com/vi/dQw4w9WgXcQ/maxresdefault.jpg",
        "views": "746,623,786 views",
        "author": "Official Rick Astley",
        "duration": "3:32",
        "resultType": "video"
    },
    {
        "id": "UC-lHJZR3Gqxm24_Vd_AJ5Yw",
        "title": "PewDiePie",
        "subscriber_count": "106M subscribers",
        "resultType": "channel"
    }
]
```

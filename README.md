![UYTS Banner](images/banner.png)

# Unlimited YouTube Search
Unlimited YouTube Search (UYTS) is a quick and easy way to search YouTube from your Python program without the need for the YouTube Data API. It's a Python port of [youtube-scrape](https://github.com/HermanFassett/youtube-scrape) by [Herman Fassett](https://github.com/HermanFassett) and has the majority of its features.

## How do I install it?
Simply clone the repo to your PC, navigate to its folder, and run `python setup.py install`. This will install UYTS and its dependencies.

## How do I use it?
You'll need to import `uyts` at the start of your project in order to use Unlimited YouTube Search. From then on, you can search YouTube using `search = uyts.Search('search query')`. This returns a search object which has the attribute `results` storing a list of Video, Playlist and Channel objects. For example, if the first result is a video, you could run `print(search.results[0].title)` to see its title. For more information, read on.

## Simple Example Program
Here's a simple program to show how easy it is to search YouTube with UYTS.
```py
import uyts

query = input("Search query: ")
search = uyts.Search(query)

for result in search.results:
    print(result.resultType +": "+result.title)
```

# Documentation

### Search class
Usage: `uyts.Search(query,minResults=0)`

Parameters:
- `query`: the string to search for
- `minResults` (optional): the minimum number of results to return. UYTS will continue making requests until it reaches this number or runs out of results. The default value of 0 will make one search request.

Attributes:
- `results`: list of search results
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

### Playlist class
Attributes:
- `id`: the ID of the playlist
- `title`: the title of the playlist
- `thumbnail_src`: the URL of the thumbnail
- `length`: the number of videos in the playlist
- `author`: the name of the creator
- `resultType`: the type of result (in this case, `playlist`)
- `ToJSON()`: returns the playlist as a JSON object

### Channel class
Attributes:
- `id`: the ID of the channel
- `title`: the name of the channel
- `subs` or `subscriber_count`: the number of subscribers the channel has
- `resultType`: the type of result (in this case, `channel`)
- `ToJSON()`: returns the channel as a JSON object
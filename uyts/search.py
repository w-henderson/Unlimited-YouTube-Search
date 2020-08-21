import requests
from urllib import parse
import json

class Search:
    def __init__(self,query,minResults=0):
        results = []
        page = 1
        while len(results) <= minResults:
            url = requests.get("https://www.youtube.com/results?q="+parse.quote(query,safe="")+"&page="+str(page))
            if url.status_code != 200:
                raise Exception("Request failed.")
            data = url.text[url.text.index("ytInitialData")+17::]
            data = data[:data.index('window["ytInitialPlayerResponse"]')-6]
            true = True; false = False
            data = eval(data)
            sectionLists = data["contents"]["twoColumnSearchResultsRenderer"]["primaryContents"]["sectionListRenderer"]["contents"]
            
            for sectionList in sectionLists:
                if "itemSectionRenderer" not in sectionList.keys():
                    continue
                for content in sectionList["itemSectionRenderer"]["contents"]:
                    try:
                        if "videoRenderer" in content.keys():
                            results.append(Video(
                                content["videoRenderer"]["videoId"],
                                content["videoRenderer"]["title"]["runs"][0]["text"],
                                content["videoRenderer"]["thumbnail"]["thumbnails"][-1]["url"],
                                content["videoRenderer"]["viewCountText"]["simpleText"],
                                content["videoRenderer"]["ownerText"]["runs"][0]["text"],
                                content["videoRenderer"]["lengthText"]["simpleText"]
                            ))
                        elif "playlistRenderer" in content.keys():
                            results.append(Playlist(
                                content["playlistRenderer"]["playlistId"],
                                content["playlistRenderer"]["title"]["simpleText"],
                                content["playlistRenderer"]["thumbnailRenderer"]["playlistVideoThumbnailRenderer"]["thumbnail"]["thumbnails"][-1]["url"],
                                content["playlistRenderer"]["videoCount"],
                                content["playlistRenderer"]["shortBylineText"]["runs"][0]["text"]
                            ))
                        elif "channelRenderer" in content.keys():
                            results.append(Channel(
                                content["channelRenderer"]["channelId"],
                                content["channelRenderer"]["title"]["simpleText"],
                                content["channelRenderer"]["subscriberCountText"]["simpleText"]
                            ))
                    except: # If at first you don't succeed, give up
                        continue
            if int(data["estimatedResults"]) < minResults:
                break
            page += 1

        self.results = results
        self.query = query
        self.resultsCount = len(results)
        self.maxResultsCount = int(data["estimatedResults"])


class Video:
    def __init__(self,id,title,thumbnail_src,views,author,duration):
        self.id = id
        self.title = title
        self.thumbnail_src = thumbnail_src
        self.views = views
        self.author = author
        self.duration = duration
        self.resultType = "video"
    def __str__(self):
        return self.title+" (id="+self.id+")"

class Playlist:
    def __init__(self,id,title,thumbnail_src,length,author):
        self.id = id
        self.title = title
        self.thumbnail_src = thumbnail_src
        self.length = length
        self.author = author
        self.resultType = "playlist"
    def __str__(self):
        return self.title+" (id="+self.id+")"

class Channel:
    def __init__(self,id,title,subscriber_count):
        self.id = id
        self.title = title
        self.subscriber_count = subscriber_count
        self.subs = subscriber_count
        self.resultType = "channel"

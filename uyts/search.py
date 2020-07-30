import requests
from urllib import parse
import json

class Search:
    def __init__(self,query):
        url = requests.get("https://www.youtube.com/results?q="+parse.quote(query,safe=""))
        if url.status_code != 200:
            raise Exception("Request failed.")
        data = url.text[url.text.index("ytInitialData")+17::]
        data = data[:data.index('window["ytInitialPlayerResponse"]')-6]
        true = True; false = False
        data = eval(data)
        print("results: "+str(data["estimatedResults"]))
        sectionLists = data["contents"]["twoColumnSearchResultsRenderer"]["primaryContents"]["sectionListRenderer"]["contents"]

        results = []
        for sectionList in sectionLists:
            if "itemSectionRenderer" not in sectionList.keys():
                continue
            for content in sectionList["itemSectionRenderer"]["contents"]:
                if "videoRenderer" in content.keys():
                    results.append(Video(
                        content["videoRenderer"]["videoId"],
                        content["videoRenderer"]["title"]["runs"][0]["text"],
                        content["videoRenderer"]["thumbnail"]["thumbnails"][-1]["url"],
                        content["videoRenderer"]["viewCountText"]["simpleText"],
                        content["videoRenderer"]["ownerText"]["runs"][0]["text"]
                    ))
                    
        self.results = results


class Video:
    def __init__(self,id,title,thumbnail_src,views,author):
        self.id = id
        self.title = title
        self.thumbnail_src = thumbnail_src
        self.views = views
        self.author = author
    def __str__(self):
        return self.title+" (id="+self.id+")"

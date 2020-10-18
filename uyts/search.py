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
            
            try: # Old YouTube parsing
                data = url.text[url.text.index("ytInitialData")+17::]
                data = data[:data.index('window["ytInitialPlayerResponse"]')-6]
                self.parseMethod = "initialData"
            except ValueError: # Scraper-compatible YouTube parsing
                data = url.text[url.text.index("// scraper_data_begin")+42::]
                data = data[:data.index('// scraper_data_end')-3]
                self.parseMethod = "scraper_data"

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

        # remove duplicate results
        foundURLs = []
        noDuplicateResults = []
        for result in results:
            if result.id not in foundURLs:
                foundURLs.append(result.id)
                noDuplicateResults.append(result)

        self.results = noDuplicateResults
        self.resultsJSON = [result.ToJSON() for result in self.results]
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
    def ToJSON(self):
        return {
            "id":self.id,
            "title":self.title,
            "thumbnail_src":self.thumbnail_src,
            "views":self.views,
            "author":self.author,
            "duration":self.duration,
            "resultType":self.resultType
        }
    def ToXML(self):
        tempJson = self.ToJSON()
        xml = '<video>'
        for key in tempJson:
            xml += "<"+key+">"+tempJson[key]+"</"+key+">"
        xml += "</video>"
        return xml

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
    def ToJSON(self):
        return {
            "id":self.id,
            "title":self.title,
            "thumbnail_src":self.thumbnail_src,
            "length":self.length,
            "author":self.author,
            "resultType":self.resultType
        }
    def ToXML(self):
        tempJson = self.ToJSON()
        xml = '<playlist>'
        for key in tempJson:
            xml += "<"+key+">"+tempJson[key]+"</"+key+">"
        xml += "</playlist>"
        return xml

class Channel:
    def __init__(self,id,title,subscriber_count):
        self.id = id
        self.title = title
        self.subscriber_count = subscriber_count
        self.subs = subscriber_count
        self.resultType = "channel"
    def ToJSON(self):
        return {
            "id":self.id,
            "title":self.title,
            "subscriber_count":self.subscriber_count,
            "resultType":self.resultType
        }
    def ToXML(self):
        tempJson = self.ToJSON()
        xml = '<channel>'
        for key in tempJson:
            xml += "<"+key+">"+tempJson[key]+"</"+key+">"
        xml += "</channel>"
        return xml
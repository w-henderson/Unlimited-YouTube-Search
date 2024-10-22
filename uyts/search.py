"""Classes and methods relating to the searching of YouTube."""

import requests
from urllib import parse
import json

class Search:
    """
    Base class for search operations, performs a search when initialised.
    """

    def __init__(self, query, language="en", country="GB", minResults=0, timeout=5):
        """Initialise search class by performing a search."""

        results = []
        page = 1
        while len(results) <= minResults:
            headers= {
                "User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
                "Accept-Language": language
            }

            url = requests.get(
                "https://www.youtube.com/results?q="+parse.quote(query,safe="")+"&page="+str(page)+"&gl="+country,
                headers=headers,
                timeout=timeout
            )
            if url.status_code != 200: raise Exception("Request failed.")
            
            try: # Old YouTube parsing
                data = url.text[url.text.index("ytInitialData")+16::]
                data = data[:data.index('</script>')-1]
                self.parseMethod = "initialData"
            except ValueError: # Scraper-compatible YouTube parsing
                data = url.text[url.text.index("// scraper_data_begin")+42::]
                data = data[:data.index('// scraper_data_end')-3]
                self.parseMethod = "scraper_data"

            data = json.loads(data)
            sectionLists = data["contents"]["twoColumnSearchResultsRenderer"]["primaryContents"]["sectionListRenderer"]["contents"]
            
            for sectionList in sectionLists:
                if "itemSectionRenderer" not in sectionList.keys():
                    continue
                for content in sectionList["itemSectionRenderer"]["contents"]:
                    try:
                        if "videoRenderer" in content.keys():
                            try:
                                accountType = content["videoRenderer"]["ownerBadges"][0]["metadataBadgeRenderer"]["style"]
                            except:
                                accountType = "regular"
                            results.append(Video(
                                content["videoRenderer"]["videoId"],
                                content["videoRenderer"]["title"]["runs"][0]["text"],
                                content["videoRenderer"]["thumbnail"]["thumbnails"][-1]["url"],
                                content["videoRenderer"]["viewCountText"]["simpleText"],
                                content["videoRenderer"]["ownerText"]["runs"][0]["text"],
                                content["videoRenderer"]["lengthText"]["simpleText"],
                                accountType = accountType
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
                            try:
                                accountType = content["channelRenderer"]["ownerBadges"][0]["metadataBadgeRenderer"]["style"]
                            except:
                                accountType = "regular"
                            results.append(Channel(
                                content["channelRenderer"]["channelId"],
                                content["channelRenderer"]["title"]["simpleText"],
                                content["channelRenderer"]["subscriberCountText"]["simpleText"],
                                accountType = accountType
                            ))
                    except: # If at first you don't succeed, give up
                        continue
            if int(data["estimatedResults"]) < minResults:
                break
            page += 1

            if len(results) == 0:
                break

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
        self.resultsCount = len(self.results)
        self.maxResultsCount = int(data["estimatedResults"])
        
        self.suggestedSearches = [] if "refinements" not in data else data["refinements"]


class Video:
    """Class representing a YouTube video."""

    def __init__(self,id,title,thumbnail_src,views,author,duration,accountType="regular"):
        self.id = id
        self.title = title
        self.thumbnail_src = thumbnail_src
        self.views = views
        self.author = author
        self.duration = duration
        self.resultType = "video"

        accountTypes = {
            "regular": "regular",
            "BADGE_STYLE_TYPE_VERIFIED_ARTIST": "music",
            "BADGE_STYLE_TYPE_VERIFIED": "verified"
        }

        self.accountType = accountTypes[accountType]

    def __repr__(self):
        return self.title+" (id="+self.id+")"

    def ToJSON(self):
        """Return the YouTube video as a JSON object."""

        return {
            "id":self.id,
            "title":self.title,
            "thumbnail_src":self.thumbnail_src,
            "views":self.views,
            "author":self.author,
            "duration":self.duration,
            "resultType":self.resultType,
            "accountType":self.accountType
        }

    def ToXML(self):
        """Return the YouTube video as an XML string."""

        tempJson = self.ToJSON()
        xml = '<video>'
        for key in tempJson:
            xml += "<"+key+">"+tempJson[key]+"</"+key+">"
        xml += "</video>"
        return xml

class Playlist:
    """Class representing a YouTube playlist."""

    def __init__(self,id,title,thumbnail_src,length,author):
        self.id = id
        self.title = title
        self.thumbnail_src = thumbnail_src
        self.length = length
        self.author = author
        self.resultType = "playlist"

    def __repr__(self):
        return self.title+" (id="+self.id+")"

    def ToJSON(self):
        """Return the YouTube playlist as a JSON object."""

        return {
            "id":self.id,
            "title":self.title,
            "thumbnail_src":self.thumbnail_src,
            "length":self.length,
            "author":self.author,
            "resultType":self.resultType
        }

    def ToXML(self):
        """Return the YouTube playlist as an XML string."""

        tempJson = self.ToJSON()
        xml = '<playlist>'
        for key in tempJson:
            xml += "<"+key+">"+tempJson[key]+"</"+key+">"
        xml += "</playlist>"
        return xml

class Channel:
    """Class representing a YouTube channel."""

    def __init__(self,id,title,subscriber_count,accountType="regular"):
        self.id = id
        self.title = title
        self.subscriber_count = subscriber_count
        self.subs = subscriber_count

        accountTypes = {
            "regular": "regular",
            "BADGE_STYLE_TYPE_VERIFIED_ARTIST": "music",
            "BADGE_STYLE_TYPE_VERIFIED": "verified"
        }

        self.accountType = accountTypes[accountType]
        self.resultType = "channel"


    def ToJSON(self):
        """Return the YouTube channel as a JSON object."""

        return {
            "id":self.id,
            "title":self.title,
            "subscriber_count":self.subscriber_count,
            "resultType":self.resultType,
            "accountType":self.accountType
        }

    def ToXML(self):
        """Return the YouTube channel as an XML string."""

        tempJson = self.ToJSON()
        xml = '<channel>'
        for key in tempJson:
            xml += "<"+key+">"+tempJson[key]+"</"+key+">"
        xml += "</channel>"
        return xml
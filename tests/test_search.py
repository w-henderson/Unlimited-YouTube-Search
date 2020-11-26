from uyts.search import Search, Video, Playlist, Channel

def queryTest(query):
    search = Search(query)
    
    assert type(search.results) == list
    assert search.parseMethod in ["initialData", "scraper_data"]
    assert search.resultsCount == len(search.results)
    assert search.query == query

    for result in search.results:
        assert type(result) in [Video, Playlist, Channel]
        assert type(result.title) == str

def test_Search():
    queries = [
        "pewdiepie", # Test something that'll bring up a channel
        "music", # Test something that'll bring up lots of playlists
        "never gonna give you up", # Test something general
        "tom scott", # Test something that'll bring up a channel
        "minecraft", # Test something general
        "o347tvnq9784tnaowitn" # Test something that'll bring up no results
    ]

    for query in queries:
        queryTest(query)
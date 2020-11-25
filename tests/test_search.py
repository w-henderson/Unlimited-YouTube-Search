from uyts.search import Search, Video, Playlist, Channel

def test_Search():
    search = Search("pewdiepie")
    
    assert type(search.results) == list
    assert search.parseMethod in ["initialData", "scraper_data", "initialDataV2"]
    assert search.resultsCount == len(search.results)
    assert search.query == "pewdiepie"

    for result in search.results:
        assert type(result) in [Video, Playlist, Channel]
        assert type(result.title) == str

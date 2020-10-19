from uyts.search import Video, Playlist, Channel

def test_Video():
    testVideo = Video(
        "dQw4w9WgXcQ",
        "Rick Astley - Never Gonna Give You Up (Video)",
        "https://i.ytimg.com/vi/dQw4w9WgXcQ/hq720.jpg",
        "782,826,227 views",
        "Official Rick Astley",
        "3:33"
    )

    assert str(testVideo) == "Rick Astley - Never Gonna Give You Up (Video) (id=dQw4w9WgXcQ)"
    assert testVideo.ToJSON() == {
        "id": "dQw4w9WgXcQ",
        "title": "Rick Astley - Never Gonna Give You Up (Video)",
        "thumbnail_src": "https://i.ytimg.com/vi/dQw4w9WgXcQ/hq720.jpg",
        "views": "782,826,227 views",
        "author": "Official Rick Astley",
        "duration": "3:33",
        "resultType": "video"
    }
    assert testVideo.ToXML() == "<video><id>dQw4w9WgXcQ</id><title>Rick Astley - Never Gonna Give You Up (Video)</\
        title><thumbnail_src>https://i.ytimg.com/vi/dQw4w9WgXcQ/hq720.jpg</thumbnail_src><views>782,826,227 views</\
        views><author>Official Rick Astley</author><duration>3:33</duration><resultType>video</resultType></video>".replace("        ","")

def test_Playlist():
    testPlaylist = Playlist(
        "PLH7-uob7X0Ab8EimH6H_5UmmLyv256axg",
        "good songs 👌",
        "https://i.ytimg.com/vi/QOy3PyRi_x0/maxresdefault.jpg",
        "22",
        "CoolTomato"
    )

    assert str(testPlaylist) == "good songs 👌 (id=PLH7-uob7X0Ab8EimH6H_5UmmLyv256axg)"
    assert testPlaylist.ToJSON() == {
        "id": "PLH7-uob7X0Ab8EimH6H_5UmmLyv256axg",
        "title": "good songs 👌",
        "thumbnail_src": "https://i.ytimg.com/vi/QOy3PyRi_x0/maxresdefault.jpg",
        "length": "22",
        "author": "CoolTomato",
        "resultType": "playlist"
    }
    assert testPlaylist.ToXML() == "<playlist><id>PLH7-uob7X0Ab8EimH6H_5UmmLyv256axg</id><title>good songs 👌</\
        title><thumbnail_src>https://i.ytimg.com/vi/QOy3PyRi_x0/maxresdefault.jpg</thumbnail_src><length>22</\
        length><author>CoolTomato</author><resultType>playlist</resultType></playlist>".replace("        ","")

def test_Channel():
    testChannel = Channel(
        "UC-lHJZR3Gqxm24_Vd_AJ5Yw",
        "PewDiePie",
        "107M subscribers"
    )

    assert testChannel.ToJSON() == {
        "id": "UC-lHJZR3Gqxm24_Vd_AJ5Yw",
        "title": "PewDiePie",
        "subscriber_count": "107M subscribers",
        "resultType": "channel"
    }
    assert testChannel.ToXML() == "<channel><id>UC-lHJZR3Gqxm24_Vd_AJ5Yw</id><title>PewDiePie</title>\
        <subscriber_count>107M subscribers</subscriber_count><resultType>channel</resultType></channel>".replace("        ","")
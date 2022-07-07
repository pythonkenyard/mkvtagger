

from sys import set_asyncgen_hooks


def get_tvdb(show,seasonepisode):
    import requests
    import json
    import time
    print("running tvdb check")
    query = show.replace(" ", "%20")

    #THIS IS ONLY REQUIRED IF THE API KEY CHANGES ("searchkey").
    # do a query to find the js query page for search results. "vendorkey" is variable.
    """
    cookies = {
        'tvdb_5ce3823a428dc': 'eyJpdiI6Im5ya28wSnhIK2pQNHRIWFRyeHpxWXc9PSIsInZhbHVlIjoiVEM5d0ErRVlJZmYrV0JUdkhyakhTK3NTaVVDQ2gxTTMrVFZsTEp4MDRNSDJYY05BdzA0cVpmMUQ4bWVqSTR4QnIwVEJRSXBNWWRYXC9JODBGXC9YSENRdz09IiwibWFjIjoiZjY0ZTk3N2M5YWExM2E2ZTM0YTQxOGQwMmRjMWQ1ODg3MGQwNTEyNjFlNWRlNmMyZmU4ZTA5ZmQ1NTQzOTdmOSJ9',
    }

    headers = {
        'authority': 'thetvdb.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'en-US,en;q=0.9,es;q=0.8,de-DE;q=0.7,de;q=0.6,it;q=0.5',
        # 'cookie': 'tvdb_5ce3823a428dc=eyJpdiI6Im5ya28wSnhIK2pQNHRIWFRyeHpxWXc9PSIsInZhbHVlIjoiVEM5d0ErRVlJZmYrV0JUdkhyakhTK3NTaVVDQ2gxTTMrVFZsTEp4MDRNSDJYY05BdzA0cVpmMUQ4bWVqSTR4QnIwVEJRSXBNWWRYXC9JODBGXC9YSENRdz09IiwibWFjIjoiZjY0ZTk3N2M5YWExM2E2ZTM0YTQxOGQwMmRjMWQ1ODg3MGQwNTEyNjFlNWRlNmMyZmU4ZTA5ZmQ1NTQzOTdmOSJ9',
        'dnt': '1',
        'referer': 'https://thetvdb.com/search',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36',
    }

    params = {
        'query': 'great irish',
    }

    jsresponse = requests.get('https://thetvdb.com/search', params=params, cookies=cookies, headers=headers)
    #print(jsresponse)
    data = jsresponse.text
    print(data)
    vendorkeystart = data.index("/build/js/vendor-") +17
    vendorkeyend = vendorkeystart+len("8e8381f002")
    vendorkey = data[vendorkeystart:vendorkeyend]
    print(vendorkey)

    #query the vendorjs page to get temp api key. key is fixed?
    headers = {
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"',
        'Referer': 'https://thetvdb.com/search?query=game+of+thrones',
        'DNT': '1',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36',
        'sec-ch-ua-platform': '"Windows"',
    }

    tdbkey = requests.get(f'https://thetvdb.com/build/js/vendor-{vendorkey}.js', headers=headers)

    data = tdbkey.text
    #print(data)
    tdbkeystart= data.index('tvshowtime') +13
    #print(str(tdbkeystart))
    tdbkeyend = tdbkeystart + len("c9d5ec1316cec12f093754c69dd879d3")
    searchkey = data[tdbkeystart:tdbkeyend]
    print(str(searchkey))
    time.sleep(0.5)"""

    #query show

    searchkey = "c9d5ec1316cec12f093754c69dd879d3"

    headers = {
        'Accept-Language': 'en-US,en;q=0.9,es;q=0.8,de-DE;q=0.7,de;q=0.6,it;q=0.5',
        'Connection': 'keep-alive',
        'DNT': '1',
        'Origin': 'https://thetvdb.com',
        'Referer': 'https://thetvdb.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36',
        'accept': 'application/json',
        'content-type': 'application/x-www-form-urlencoded',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    data = '{"requests":[{"indexName":"TVDB","params":"query='+query+'&maxValuesPerFacet=10&page=0&highlightPreTag=__ais-highlight__&highlightPostTag=__%2Fais-highlight__&facets=%5B%22type%22%2C%22year%22%2C%22network%22%2C%22status%22%2C%22type%22%2C%22year%22%2C%22network%22%2C%22status%22%5D&tagFilters="}]}'

    response = requests.post(f'https://tvshowtime-dsn.algolia.net/1/indexes/*/queries?x-algolia-agent=Algolia%20for%20vanilla%20JavaScript%20(lite)%203.32.0%3Binstantsearch.js%20(3.5.3)%3BJS%20Helper%20(2.28.0)&x-algolia-application-id=tvshowtime&x-algolia-api-key={searchkey}', headers=headers, data=data)
    #print(response)
    #print(response.txt)
    response = response.json()
    possiblemovie = 1
    printtable = [["No.","Year","Title","TVDBid", "info"]]
    for i in response['results'][0]['hits']:
        tvdbid = i['id']
        title = i['name']
        try:
            year = i['year']
        except:
            year = "????"
        try:
            info = i["overview"]
        except:
            info = " "
        printtable.append([f"({possiblemovie})",str(year),title,str(tvdbid),info])
        possiblemovie += 1
    print("\nTVDB QUERY RESULTS:\n")
    for row in printtable:
        print("{: <3} {: <4} {: <36} {: <8} {: <50}".format(*row))
    print(f"({possiblemovie}) - NONE MATCH")

    if possiblemovie <3:
        choice = 0
    else:
        choice = int(input(f"Select TVDB match\n option 1-{possiblemovie}: ")) -1

    try:
        selectedtvshow = response['results'][0]['hits'][choice]
        tvdbid = selectedtvshow['id']
        title = selectedtvshow['name']
        slug = selectedtvshow['slug']
        print(f"\n\n{title}, {tvdbid}")
    except:
        tvdb = [" ", " ", " ", " ", " "]
        return tvdb

    cookies = {
        'TVDB_AUTHENTICATED': 'eyJpdiI6Ikh0WEQ5TXpnSHRYQ1lHa2tXWlNJbUE9PSIsInZhbHVlIjoiQ0ptMHZSZDZyZEZDOVAxREtLbW1EZz09IiwibWFjIjoiYmVmOTEzNmI3NjE1YTY5YWUxMjUzYzFmMjU0MjQyMWY5NzEyNjEwZmQwYWY5ZjU0MmJkYzQxOWUyNTcwMGIwZSJ9',
        'tvdb_5ce3823a428dc': 'eyJpdiI6InB3ZUhTNTNwdkVob0p5eFRDM2ZqclE9PSIsInZhbHVlIjoiQ2RNaDJhRDZIeDdqSG9UWTZRT0tORTNuYXc3XC9QS0pESTVNXC9ic2NcL1J2YkhtXC9HcHFJc2VBOWlENnNlT0VHcVlhMWJvNkp2WjNnY01zbFowOVhtZ3RBPT0iLCJtYWMiOiJiOGMzYzUyOWY0MDA4NDYxNjIyYWRhNTBkOWVmZjMxMDg0NzY2MDM5MzJiNjFjN2NkYTk4ODA4ODU2NDI2NzUyIn0%3D',
    }

    headers = {
        'authority': 'thetvdb.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'en-US,en;q=0.9,es;q=0.8,de-DE;q=0.7,de;q=0.6,it;q=0.5',
        # Requests sorts cookies= alphabetically
        # 'cookie': 'TVDB_AUTHENTICATED=eyJpdiI6Ikh0WEQ5TXpnSHRYQ1lHa2tXWlNJbUE9PSIsInZhbHVlIjoiQ0ptMHZSZDZyZEZDOVAxREtLbW1EZz09IiwibWFjIjoiYmVmOTEzNmI3NjE1YTY5YWUxMjUzYzFmMjU0MjQyMWY5NzEyNjEwZmQwYWY5ZjU0MmJkYzQxOWUyNTcwMGIwZSJ9; tvdb_5ce3823a428dc=eyJpdiI6InB3ZUhTNTNwdkVob0p5eFRDM2ZqclE9PSIsInZhbHVlIjoiQ2RNaDJhRDZIeDdqSG9UWTZRT0tORTNuYXc3XC9QS0pESTVNXC9ic2NcL1J2YkhtXC9HcHFJc2VBOWlENnNlT0VHcVlhMWJvNkp2WjNnY01zbFowOVhtZ3RBPT0iLCJtYWMiOiJiOGMzYzUyOWY0MDA4NDYxNjIyYWRhNTBkOWVmZjMxMDg0NzY2MDM5MzJiNjFjN2NkYTk4ODA4ODU2NDI2NzUyIn0%3D',
        'dnt': '1',
        'referer': 'https://thetvdb.com/search?query='+query,
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36',
    }

    response = requests.get('https://thetvdb.com/series/'+slug, cookies=cookies, headers=headers)

    try:
        seriesdata = response.text
        seriesdata = seriesdata.split('"change_translation_text" data-language="eng"')
        seriesdatastart = seriesdata[1].index("<p>") +3
        seriesdatafinish = seriesdata[1].index("</p>")
        seriesinformation = seriesdata[1][seriesdatastart:seriesdatafinish]
        print(seriesinformation)
    except:
        seriesinformation = " "
        print("no series information")
    try:
        seriesdata = seriesdata[1].split('/series/'+slug+'/artwork/banners')
        seriesdatastart = seriesdata[1].index("href=") +6
        seriesdatafinish = seriesdata[1].index('" class="thumbnail')
        seriesjpeg = seriesdata[1][seriesdatastart:seriesdatafinish]
        print(seriesjpeg)
    except:
        print("no series thumbnail")
        seriesjpeg = " "


    import requests

    cookies = {
        'TVDB_AUTHENTICATED': 'eyJpdiI6Ikh0WEQ5TXpnSHRYQ1lHa2tXWlNJbUE9PSIsInZhbHVlIjoiQ0ptMHZSZDZyZEZDOVAxREtLbW1EZz09IiwibWFjIjoiYmVmOTEzNmI3NjE1YTY5YWUxMjUzYzFmMjU0MjQyMWY5NzEyNjEwZmQwYWY5ZjU0MmJkYzQxOWUyNTcwMGIwZSJ9',
        'tvdb_5ce3823a428dc': 'eyJpdiI6IndHUWx3RmVDYlFZYVJSVks1Z1pmU2c9PSIsInZhbHVlIjoid3YwRk54c05tVW0xYmVpK0dMY2o5clRlbTFJZ29ySm15blljRjdEbndQd2xiOUhuV1BPTVZJdVwvYXRBQk5QUkFENTlHbDBOUk00ZUZhcGx3Qno1S0VnPT0iLCJtYWMiOiI4MGQ4NWRjYTY1ZDZhZGUwN2E3NmI0MjNlNzhmY2I2M2UzYmM1NzY2ZTBkYjExZmIzNWI5ZWM4YjRmZmM5ZjM5In0%3D',
    }

    headers = {
        'authority': 'thetvdb.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'en-US,en;q=0.9,es;q=0.8,de-DE;q=0.7,de;q=0.6,it;q=0.5',
        'dnt': '1',
        'referer': 'https://thetvdb.com/series/'+slug,
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36',
    }

    response = requests.get(f'https://thetvdb.com/series/{slug}/allseasons/official', cookies=cookies, headers=headers)

    episodedata = response.text
    try:
        episodedata = episodedata.split(seasonepisode)
        episodedatastart = episodedata[1].index("<p>") +3
        episodedatafinish = episodedata[1].index("</p>")
        episodeinformation = episodedata[1][episodedatastart:episodedatafinish]
        print(episodeinformation)
    except:
        episodeinformation = " "
    try:
        episodedatastart = episodedata[1].index("img data-src=") +14
        episodedatafinish = episodedata[1].index("jpg")+3
        episodejpeg = episodedata[1][episodedatastart:episodedatafinish]
        print(episodejpeg)
    except:
        episodejpeg = " "
    tvdb = [tvdbid, seriesinformation, seriesjpeg, episodeinformation, episodejpeg]
    return tvdb


if __name__ == "__main__":
    title = input("Input the title of series or movie you are searching for:")
    season = int(input("Input the Season number: ")).zfill(2)
    episode = int(input("Input the episode: ")).zfill(2)
    seasonepisode = f"S{season}E{episode}"

    get_tvdb(title, seasonepisode)

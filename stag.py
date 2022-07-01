import os
import sys
import re
import time
from tkinter import filedialog
import tkinter as tk

import requests
from guessit import guessit
import tvdb
import imdb

#add tmdb api key
tmdb_api_key = ""

class tagger:
    def __init__(self, folder):
        self.folder = folder
        self.files = os.listdir(self.folder)
        self.tmdb_api_key = tmdb_api_key
    
        self.target = []
        #Create a list of the download mp4 files
        for file in self.files:
            if file.endswith(".mkv"):
                self.target.append(file)

        #gather prerequisite data
        self.targetinfo = guessit(self.files[0])
        self.title = self.targetinfo['title']

        print(self.title)

    #imdb
    def imdb(self):
        ia = imdb.Cinemagoer()
        try:
            movies = ia.search_movie(self.title)
            #print(str(movies))
            if len(movies) <1:
                print("no result from IMDB check")
                raise
            elif len(movies) == 1:
                print("one result")
                self.imdbnum = movies[0].movieID
                self.imdbtitle = movies[0]["title"]
                self.imdbyear = movies[0]["year"]
            elif len(movies)>1:
                possiblemovie = 1
                printtable = [["No.","Year","Title","IMDb"]]

                for movie in movies:
                    selectchoice = possiblemovie-1
                    try:
                        year = movies[selectchoice]["year"]
                    except:
                        year = "0000"
                    title = movies[selectchoice]["title"]
                    id = movies[selectchoice].movieID
                    printtable.append([f"({possiblemovie})",str(year),title,str(id)])
                    possiblemovie += 1
                x="n"
                while x == "n":
                    x="y"
                    print("\nIMDB QUERY TABLE\n")
                    for row in printtable:
                        print("{: <4} {: <5} {: <35} {: <10} ".format(*row))
                    print(f"({possiblemovie}) - NO MATCH")
                    choice = int(input(f"Select correct option 1-{possiblemovie}: ")) -1
                    try:
                        self.imdbnum = movies[choice].movieID
                        self.imdbtitle = movies[choice]["title"]
                        self.imdbyear = movies[choice]["title"]
                        try:
                            movie = ia.get_movie(self.imdbnum, info=['taglines', 'plot'])

                            try:
                                plot = movie['plot'][0]
                                print("\nPLOT\n"+plot)
                            except:
                                print("Plot unknown or not possible to search.")
                            try:
                                synopsis = movie['synopsis'][0]
                                print("\nSYNOPSIS\n"+synopsis)
                            except:
                                print("Synopsis unknown")
                            x=input("is this correct?[y/n] :").lower()
                            if x == "n":
                                os.system("cls")
                            elif x == "y":
                                continue
                            else:
                                print("Invalid selection")
                                time.sleep(1)
                                x = "n"
                        except:
                            pass
                    except:
                        print("failed to assign IMDB reference")
                        self.imdbnum, self.imdbtitle, self.imdbyear = "1", "None", "0000"
        except:
            try:
                #todo add support for searching and adding multiple from here
                title = title.replace(" ", "%20")
                response = requests.get(rf"https://imdb-api.com/en/API/SearchSeries/k_p1b27972/{title}").json()
                print("this is the tv search "+str(response))
                self.imdbnum = response["results"]["0"]["id"]
                self.imdbtitle = response["results"]["0"]["title"]
                self.imdbyear = response["results"]["0"]["description"]
            except:
                print("No IMDB Match")
                self.imdbnum, self.imdbtitle, self.imdbyear = "1", "None", "0000"
    
    #tmdb
    def tvdb(self):
        try:
            episode = self.targetinfo['episode']
            episode = str(episode).zfill(2)
        except:
            episode = "01"
        try:
            season = self.targetinfo['season']
            season = str(season).zfill(2)
        except:
            season = " "
        try:
            seasonepisode = f"S{season}E{episode}"
            #print(seasonepisode)
            tvdbdata = tvdb.get_tvdb(self.title,seasonepisode)
            print("gathered tvdb data")
            #print(str(tvdbdata))
        except:
            print("no tvdb information available")

        try:
            self.tvdbid = tvdbdata[0]

        except:
            self.tvdbid = "1"

    #tvdb
    def tmdb(self):
        #f'https://api.themoviedb.org/3/find/tt0805418?api_key={self.tmdb_api_key}&language=en-US&external_source=tvdb_id'
        try:
            tmdbrequest = requests.get(url=f"https://api.themoviedb.org/3/find/tt{self.imdbnum}?api_key={self.tmdb_api_key}&language=en-US&external_source=imdb_id").json()
            #print(tmdbrequest)
            try:
                print("checking movie results")
                self.tmdbid = tmdbrequest["movie_results"][0]["id"]
                self.tmdb_desc = tmdbrequest["movie_results"][0]["overview"]
                self.tmdb_type = "movie"
            except:
                print("checking tv results")
                self.tmdbid = tmdbrequest["tv_results"][0]["id"]
                self.tmdb_desc = tmdbrequest["tv_results"][0]["overview"]
                self.tmdb_type = "tv"
        except:
            print(f"Failed cross-checking TMDB against IMDB (no result?).\nUsing direct search for {self.title}.")
            filetitle = self.title.replace(" ","+")
            tmdbrequest = requests.get(url = f"https://api.themoviedb.org/3/search/movie?api_key={self.tmdb_api_key}&query={filetitle}").json()
            tmdblist = [["No.","Year", "Title","tmdbid","desc"]]
            tmdblist2 = [["No.","Year", "Title","tmdbid","desc"]]
            try:
                tmdbselection = 1
                for i in tmdbrequest["results"]:
                    id = i["id"]
                    title = i["title"]
                    year = i["release_date"]
                    year = year[0:4]
                    overview = i["overview"]
                    overviewabbv = overview[:60]
                    tmdblist.append([f"({tmdbselection})", year, title, id, overviewabbv])
                    tmdbselection += 1
                tvdivider = tmdbselection
                print(str(tvdivider))
                for row in tmdblist:
                    print("{: <4} {: <5} {: <30} {: <5} {: <60}".format(*row))
                tmdbrequest2 = requests.get(url = f"https://api.themoviedb.org/3/search/tv?api_key={self.tmdb_api_key}&query={filetitle}").json()
                print("Possible tv matches")
                try:
                    for i in tmdbrequest2["results"]:
                        id = i["id"]
                        title = i["name"]
                        overview = i["overview"]
                        year = i["first_air_date"]
                        year = year[0:4]
                        overviewabbv = overview[:60]
                        tmdblist.append([f"({tmdbselection})",year, title, id, overviewabbv])
                        tmdblist2.append([f"({tmdbselection})",year, title, id, overviewabbv])
                        tmdbselection += 1

                    for row in tmdblist2:
                        print("{: <4} {: <5} {: <30} {: <5} {: <40}".format(*row))
                    print(f"({tmdbselection}) - NO MATCH ABOVE")
                except:
                    print("no matches")
                if tmdbselection > 1:
                    if tmdbselection ==2:
                        print("single result. Automatically assigning tmdb tv show id")
                        choice = 1
                    else:
                        choice = int(input(f"Select matching TMDB option 1-{tmdbselection}: "))
                else:
                    print("No matches on TMDB either.")
                    choice = 1
                if choice < tvdivider:
                    try:
                        choice -= 1
                        self.tmdbid = tmdbrequest["results"][choice]["id"]
                        self.tmdb_desc = tmdbrequest["results"][choice]["overview"]
                        self.tmdb_type = "movie"
                    except:
                        print("Not possible to assign due to error")
                else:
                    choice-= tvdivider
                    try:
                        self.tmdbid = tmdbrequest2["results"][choice]["id"]
                        self.tmdb_desc = tmdbrequest2["results"][choice]["overview"]
                        tmdb_type = "tv"
                    except:
                        print("No TMDB picked. Assigning id of 1")
                        self.tmdbid, self.tmdb_desc, self.tmdb_type = "1", "none", "none"

            except:
                print("failed getting tmdb id. is your api key correct")
                self.tmdbid, self.tmdb_desc, self.tmdb_type = "1", "none", "none"
        print(f"TMDB Id found to be {self.tmdbid}")

    def formatxmldata(self):
        #print(f"{self.imdbnum}, {self.tmdbid}, {self.tvdbid}")

        with open("stags.xml", "r") as f:
            self.xmldata = f.read()
        
        f.close()

        try:
            if len(self.imdbnum)>2:
                self.writedata = self.xmldata.replace("imdbstring", self.imdbnum)
        except:
            removeimdb = re.search("(\s*<Simple>\s*.*IMDB.*\s.*\s.*\s*)<Simple>", self.xmldata)
            #print(removeimdb.group(1))
            self.writedata = self.xmldata.replace(removeimdb.group(1), "")
        try:
            if len(str(self.tmdbid))>2:
                self.writedata = self.writedata.replace("tmdbstring", str(self.tmdbid))
        except:
            removetmdb = re.search("(\s*<Simple>\s*.*TMDB.*\s.*\s.*\s*)<Simple>", self.writedata)
            #print(removetmdb.group(1))
            self.writedata = self.writedata.replace(removetmdb.group(1), "")
        try:
            if len(str(self.tvdbid))>2:
                self.writedata = self.writedata.replace("tvdbstring", str(self.tvdbid))
        except:
            removetvdb = re.search("(\s*<Simple>\s*.*TVDB.*\s.*\s.*<\/Simple>)", self.writedata)
            #print(removetvdb.group(1))
            self.writedata = self.writedata.replace(removetvdb.group(1), "")
        

    def search(self):
        self.imdb()
        
        if len(self.tmdb_api_key) >1:
            self.tmdb()
        else:
            self.tmdb_api_key = str(input("no tmdb api key detected. Please edit in the script and run again or enter it now: "))
            self.tmdb()
        self.tvdb()
        print(f"TMDB: {self.tmdbid}")
        print(f"IMDB: {self.imdbnum}")
        print(f"TVDB: {self.tvdbid}")
    #add tags
    def tags(self):
        totalepisodes = len(self.target)    
        for file in self.target:
            episodewritedata = self.writedata
            findseasonepisode = re.search('\.S(\d+)E(\d+)\.',file)
            thisseason = findseasonepisode.group(1)
            thisseason = thisseason.zfill(1)
            thisepisode = findseasonepisode.group(2)
            thisepisode = thisepisode.zfill(1)

            episodewritedata = episodewritedata.replace("season", thisseason)
            episodewritedata = episodewritedata.replace("totalepisodes", str(totalepisodes))
            episodewritedata = episodewritedata.replace("thisepisode", thisepisode)

            #print(episodewritedata)
            with open("tags.xml", "w") as g:
                g.write(episodewritedata)
            g.close()
            os.system(f'mkvpropedit "{self.folder}/{file}" --edit info --set "title={file}" --edit track:a1 --set language=eng')
            os.system(f'mkvpropedit "{self.folder}/{file}" --tags global:tags.xml')
            print(f"{file} updated")




if __name__ == "__main__":
    try:
        folder = sys.argv[2]
    except:
        root = tk.Tk()
        root.withdraw()
        folder = filedialog.askdirectory(title="Please select the series folder with files to tag")
    print(f"directory is {folder}")
    r = tagger(folder)    
    r.search()
    r.formatxmldata()
    r.tags()
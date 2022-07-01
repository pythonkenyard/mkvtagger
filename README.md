# mkvtagger
Tags .mkv file of a tv series with IMDB, TMDB and TVDB ID tags. For full season packs can also include season/episode tagging  


## Setup   
1. Install prequisites with pip install -r requirements.txt    
2. Add your tmdb api key in line ~14 of stag.py and eptag.py   
e.g tmdb_api_key = "123456789abcdef"   
3. run with "python eptag.py"   
select file to tag and confirm the imdb and tmdb/tvdb info if/as required.   
stag.py should only be used for a full season of files. If you run python stag.py it will ask you to confirm the folder the files are in. All mkv files in the folder will be updated and season info will be added. It counts the total episodes to confirm the total   
   
media info will be updated with info e.g.   
   
Note track Position and Track Total can only be added by stag.py   
This requires a full season pack to be present to add tags as it counts the total episodes to confirm the total   
   
# Example of Media info output for 1 file after running stag.py
General   
Unique ID                                : 62443573869635734601668401503009219543 (0x11FC914FBFF4149E8C6FAA8253CEA3D7)   
Complete name                            : Sarah.Beenys.Little.House.Big.Plans.S01E01.1080p.mkv   
Format                                   : Matroska   
Format version                           : Version 4   
File size                                : 1.68 GiB   
Duration                                 : 46 min 57 s   
Overall bit rate mode                    : Variable   
Overall bit rate                         : 5 110 kb/s   
Movie name                               : Sarah.Beenys.Little.House.Big.Plans.S01E01.1080p.mkv   
Track name/Position                      : 01   
Track name/Total                         : 6   
Encoded date                             : UTC 2022-06-30 19:57:05   
Writing application                      : mkvmerge v67.0.0 ('Under Stars') 64-bit   
Writing library                          : libebml v1.4.2 + libmatroska v1.6.4   
Cover                                    : Yes  
Attachments                              : cover  
IMDB                                     : tt21030356   
TMDB                                     : tv/204005   
TVDB                                     : 421055   

## Note the fields added   
Movie name                               : Sarah.Beenys.Little.House.Big.Plans.S01E01.1080p.mkv   
Track name/Position                      : 01    
Track name/Total                         : 6    
IMDB                                     : tt21030356    
TMDB                                     : tv/204005    
TVDB                                     : 421055      
   
File has movie name added which will match the file title   
track position is the episode, track total is the total amount of files in the folder (so only use stag.py for complete season packs)   
imdb tag, tmdb tag, tvdb tag

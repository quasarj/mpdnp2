"""
    Module to retrieve a song from google/youtube.
    Depends on google module, from: https://github.com/MarioVilas/google
"""
from google2 import search


def get_song_url(song):
    try:
        return search('site:youtube.com {}'.format(song), 
                      stop=1, 
                      pause=0).next()  
    except:
        return "No youtube video found :("
    

if __name__ == '__main__':
    #song = "Modest Mouse - Float On"
    song = "Coldplay - Yellow"
    #song = "Test of Time - Warez Song"
    # song = "fkgherickj592udjgkaskj98"
    print get_song_url(song)

from jikanpy import Jikan
import time
import csv


jikan = Jikan()

# This is for the full anime list
def getAnimeList(ids):

    """
    Get the csv list of animes with ids till the given parameter

    headers:
    animeID: id of anime as in anime url https://myanimelist.net/anime/ID
    name: title of anime
    premiered: premiered on. default format (season year) 
    genre: list of genre
    type: type of anime (example TV, Movie etc) 
    episodes: number of episodes
    studios: list of studio
    source: source of anime (example original, manga, game etc) 
    scored: score of anime
    scoredBy: number of member scored the anime
    members: number of member added anime to their list 
    """
    headers = ['id', 'title', 'type', 'source', 'image_url', 'episodes', 'status', 'airing', 'duration', 'rating', 'score', 'scored_by', 'rank', 'popularity', 'members', 'favorites', 'producers', 'licensors', 'studios', 'premiered', 'opening_themes', 'ending_themes', 'genres']

    with open('animeList.csv', 'w', newline ='') as f:
        write = csv.writer(f)
        write.writerow(headers)
        for a in range(1,ids):
            try:
                cc = jikan.anime(id=a)
                gen = [i['name'] for i in cc['genres']]
                producers = [i['name'] for i in cc['producers']]
                licensors = [i['name'] for i in cc['licensors']]
                studios = [i['name'] for i in cc['studios']]
                    
                ll = [cc['mal_id'], cc['title'], cc['type'], cc['source'], cc['image_url'], cc['episodes'], cc['status'], cc['airing'], cc['duration'], cc['rating'],  cc['score'], cc['scored_by'], cc['rank'], cc['popularity'], cc['members'], cc['favorites'], producers, licensors, studios, cc['premiered'], cc['opening_themes'], cc['ending_themes'], gen ]
                write.writerow(ll)    
            except Exception:
                pass  
            time.sleep(1)

if __name__ == '__main__':

    getAnimeList(50000)
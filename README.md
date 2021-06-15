# Anime-User dataset crawler
This repo contains the file used to create the dataset which contains the animelist from the [**MyAnimeList**](https://myanimelist.net/) website as well as the userdata.
It uses python as the underlying language and an unofficial MAL API [Jikan](https://jikan.docs.apiary.io/) to scrape the data as well as BeautifullSoup4.


#### Get anime list:
For the anime list file you just need a range to go through the mal_id from 1 till the user limit.

Just edit the input in the file under the function call in the main function.

#### Column metadata:
* animeID: id of anime as in anime url https://myanimelist.net/anime/ID
* name: title of anime
* premiered: premiered on. default format (season year) 
* genre: list of genre
* type: type of anime (example TV, Movie etc) 
* episodes: number of episodes
* studios: list of studio
* source: source of anime (example original, manga, game etc) 
* scored: score of anime
* scoredBy: number of member scored the anime
* members: number of member added anime to their list

#### Get user data:
For the userdata you can use the following script to get all the userdata. This script uses Jikan API to get the data as well as BS4 to get the usernames from the MAL website directly as you need the username to get the user data directly.

#### Column metadata:
* user_id: id of user
* username: username of the user
* gender: gender of the user 
* birthday: birthday of the user
* location: location of the user 
* joined: date joined
* days_watched: days spent watching,
* mean_score: mean score rated,
* watching: total animes currently watching,
* completed: total anime completed,
* on_hold: total anime on hold,
* dropped: total anime dropped,
* plan_to_watch: anime planned to watch,
* total_entries: total animes,
* rewatched: animes rewatched,
* episodes_watched: total episodes watched

#### Syntax
```
python getUser.py UserList.txt user.csv
```

#### How to create User List from forum post:
For this you need to get topic ID.
Go to [**MAL**](https://myanimelist.net/) -> [**Community** -> **Forums**](https://myanimelist.net/forum/) -> **Select a forum**

For example for the following forums links their respective ID are highlighted in bold below:

[https://myanimelist.net/forum/?topicid=1699126](https://myanimelist.net/forum/?topicid=1699126) -> **1699126**

[https://myanimelist.net/forum/?topicid=1696289](https://myanimelist.net/forum/?topicid=1696289) -> **1696289**

After getting the topic ID, you can use **createUserListFromPost** script.

###### Syntax:
```
python getUserFromPost.py topicID UserList.txt
```

#### How to create User List from club:
For this you need to get club ID.
Go to [**MAL**](https://myanimelist.net/) -> [**Community** -> **Clubs**](https://myanimelist.net/forum/) -> **Select a club**

For example for the following clubs links their respective ID are highlighted in red below:

[https://myanimelist.net/clubs.php?cid=72250](https://myanimelist.net/clubs.php?cid=72250) -> **72250**

[https://myanimelist.net/clubs.php?cid=32683](https://myanimelist.net/clubs.php?cid=32683) -> **32683**

After getting the topic ID, you can use **createUserListFromClub** script.

###### Syntax:
```
python getUserFromClub.py clubID UserList.txt
```
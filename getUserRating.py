from jikanpy import Jikan
import time
import csv
import sys
import os

"""
    Get the total details of the user and append it to a csv file.

    parameters: 
        user: username of the specific user.
    
    headers:
    user_id: id of user
    username: username of the user
    gender: gender of the user 
    birthday: birthday of the user
    location: location of the user 
    joined: date joined
    'days_watched': days spent watching,
    'mean_score': mean score rated,
    'watching': total animes currently watching,
    'completed': total anime completed,
"""

jikan = Jikan()

count = 0



header = ['username', 'anime_id', 'type', 'score', 'watched_episodes', 'start_date', 'end_date', 'watching_status', 'is_rewatching', 'tags']


if __name__ == '__main__':
    try:
        userListFile = str(sys.argv[1]) # file name for userlist
    except IndexError:
        print('Please provide all arguments.\nSyntax:\npython getUser.py UserList.txt [User.csv]')
        sys.exit()
    except:
        print('Unexpected error.')

    # setting name of output file
    if(len(sys.argv) == 3):
        outputFileName = str(sys.argv[2])
    else:
        outputFileName = 'UserRating.csv'

    f = open(userListFile, 'r') # opening file containing username in read mode
    w = open(outputFileName, 'a', newline ='',encoding='utf8')

    ww = csv.writer(w)
    if os.stat(outputFileName).st_size == 0:
        ww.writerow(header)

    for line in f:
        username = line.strip()
        print("Reading " + username + " AnimeList...\n")
        
        try:
            userAnimeList = jikan.user(username=username, request='animelist')
                
            for i in range (1, len(userAnimeList['anime'])):
                ll =[username,
                        userAnimeList['anime'][i]['mal_id'],
                        userAnimeList['anime'][i]['type'],
                        userAnimeList['anime'][i]['score'],
                        userAnimeList['anime'][i]['watched_episodes'],
                        userAnimeList['anime'][i]['start_date'],
                        userAnimeList['anime'][i]['end_date'],
                        userAnimeList['anime'][i]['watching_status'],
                        userAnimeList['anime'][i]['is_rewatching'],
                        userAnimeList['anime'][i]['tags']]
                ww.writerow(ll)
            time.sleep(1)
            count += 1
        except:
            print("ERROR getting " + username + "\n")
            pass

        print('Fetching next....\n')

        if count % 10 == 0:
            print("appended " + str(count) + " files.\n")


    f.close()
    w.close()

    print('Total', count, 'user data fetched. No more user left in', userListFile, '\nDone.\nOutput file:', outputFileName)

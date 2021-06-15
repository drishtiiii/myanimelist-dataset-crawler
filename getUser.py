from jikanpy import Jikan
import time
import csv
import sys
import os

jikan = Jikan()

count = 0

def getUserList(user):
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
    'on_hold': total anime on hold,
    'dropped': total anime dropped,
    'plan_to_watch': anime planned to watch,
    'total_entries': total animes,
    'rewatched': animes rewatched,
    'episodes_watched': total episodes watched
    """
    userlist = jikan.user(username=user)
                
    ll = [userlist['user_id'], userlist['username'], userlist['gender'], userlist['birthday'], userlist['location'], userlist['joined'], userlist['anime_stats']['watching'], userlist['anime_stats']['completed'], userlist['anime_stats']['on_hold'], userlist['anime_stats']['dropped'],  userlist['anime_stats']['plan_to_watch'], userlist['anime_stats']['total_entries'], userlist['anime_stats']['days_watched'], userlist['anime_stats']['rewatched'], userlist['anime_stats']['episodes_watched'], userlist['anime_stats']['mean_score']]

    time.sleep(1)
    
    return ll

header = ['user_id', 'username', 'gender', 'birth_date', 'location', 'joined', 'watching', 'completed', 'on_hold', 'dropped',  'plan_to_watch', 'total_entries', 'days_watched', 'rewatched', 'episodes_watched', 'mean_score']


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
        outputFileName = 'UserList.csv'

    f = open(userListFile, 'r') # opening file containing username in read mode
    w = open(outputFileName, 'a', newline ='',encoding='utf8')

    ww = csv.writer(w)
    if os.stat(outputFileName).st_size == 0:
        ww.writerow(header)

    for line in f:
        username = line.strip()
        print("Reading " + username + " AnimeList...\n")
        
        try:
            row = getUserList(username)
            ww.writerow(row)
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

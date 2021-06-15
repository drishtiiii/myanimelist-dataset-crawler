from bs4 import BeautifulSoup
import requests
import sys

try:
	topicID = str(sys.argv[1])
except IndexError:
	print('Please provide all arguments.\nSyntax:\npython creteUserListFromPost.py topicID [UserList.txt]')
	sys.exit()
except:
	print('Unexpected error.')

# setting output file
if(len(sys.argv) == 3):
	outputFile = str(sys.argv[2])
else:
	outputFile = 'UserList.txt'

f = open(outputFile, 'a') # opening output file in append mode

i = 0 # initial comment counter
usernames = set() # user set

while(True):
	print('\nFetching users from comment', i, 'through comment', i + 50, '...') # console message number of comments

	url = 'https://myanimelist.net/forum/?topicid='+ topicID + '&show=' + str(i) # base url

	page = requests.get(url) # getting page

	if(page.status_code == 200):
		c = page.content
		soup = BeautifulSoup(c, 'html.parser') # parsing page

		print('If the username already exist they will not add it to the set otherwise new username will be added.')
		print('Getting username:')
		# getting username in the page
		users = soup.find_all('td', 'forum_boardrow2')
		for j in range(0, len(users)):
			print(users[j].div.div.a.text)
			usernames.add(users[j].div.div.a.text) # adding user if only doesn't exist in the set previously

		i = i + 50 # increamenting comment count
	else:
		print('No more page left in the forum. Done fetching...\n')
		break

print('Got', len(usernames), 'unique user.')
# Writing unique username in the output file
for username in usernames:
	f.write(username + '\n')

f.close() # closing file

print('Done writing username to output file.\nOutput:', outputFile) 
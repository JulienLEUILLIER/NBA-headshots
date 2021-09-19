import os
import requests
from bs4 import BeautifulSoup

def create_dir(path):
   """Create folders"""
   try:
      if not os.path.exists(path):
         os.makedirs(path)
   except OSError:
      print('Error creating dir')

def parseNameToMatchURL(name):
      ## parse name to match url requirements, e.g : 'dallas-mavericks' or 'luka-doncic'
   return '-'.join(name.split(' '))

def getParsedHTML(errorMessage, searchTerm = ''):
   url = 'https://www.2kratings.com/teams/' + searchTerm
   header = {'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0'}

   result = requests.get(url, headers=header)

   if result.status_code == 200:
      soup = BeautifulSoup(result.content, 'html.parser')
   else:
      print(errorMessage)
      exit()

   return soup

def getAllTeamsNames():
   parsedHTML = getParsedHTML('Error with HTML parsing for teams names')

   teamsArray = []
   
   ulListOfCurrentTeams = parsedHTML.find('ul', id='ui-current-teams')
   for tag in ulListOfCurrentTeams.find_all('a', class_='sidebar-link'):
      if tag.text != ' All Current Teams':
         teamsArray.append(tag.text[1:])

   return teamsArray

def getTeamPlayers(teamName):
   parsedTeamName =  parseNameToMatchURL(teamName)

   parsedHTML = getParsedHTML('Error getting team page html', parsedTeamName)

   teamPlayers = []

   playersTable = parsedHTML.find(class_='h-100')

   for tag in playersTable.find_all('img', class_='entry-photo'):
      try:
         playerName = tag['title']
         teamPlayers.append(playerName)
      except Exception as e:
         print(e)

   return teamPlayers

def saveImage(playerName):
   try:
      url = f'https://www.2kratings.com/wp-content/uploads/{playerName}-2K-Rating.png'
      image_data = requests.get(url).content
   except Exception as e:
      pass

   with open(os.path.join(os.getcwd(), f'{playerName}.png'), 'wb') as handler:
      handler.write(image_data)

def main():
   teamsArray = getAllTeamsNames()

   mainPath = os.getcwd()

   for team in teamsArray:
      directoryPath = f'{team}'
      os.chdir(mainPath)
      create_dir(directoryPath)
      os.chdir(directoryPath)

      playersArray = getTeamPlayers(team)

      for player in playersArray:
         try:
            parsedPlayerName = parseNameToMatchURL(player)
            saveImage(parsedPlayerName)
         except Exception as e:
            print(e)

if __name__ == "__main__":
   main()

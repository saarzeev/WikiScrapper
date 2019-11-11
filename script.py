from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

###### Question 1
wiki_prefix = "https://en.wikipedia.org/"
wiki = "https://en.wikipedia.org/wiki/Julia_Roberts_filmography"
page = urlopen(wiki)

soup = BeautifulSoup(page, features="html.parser")

jr_movies_table = soup.find_all("table")[0]

#Build df
A=[]
B=[]
C=[]
D=[]
movies_links = []


for row in jr_movies_table.findAll("tr"):
    cells = row.findAll('td')
    movies=row.findAll('th') #To store second column data
    if len(cells) == 5: #Only extract table body not heading

        A.append(movies[0].find(text=True))
        B.append(int(cells[0].find(text=True)))
        C.append(cells[1].find(text=True))
        D.append(cells[2].find(text=True))


        link = movies[0].a
        if not link:
            movies_links.append("")
        for link in movies[0].findAll('a'):
            movies_links.append(wiki_prefix + link.get('href'))

#import pandas to convert list to data frame
import pandas as pd

df=pd.DataFrame(A,columns=['Title'])
df['Year']=B
df['Role']=C
df['Director']=D
df['Links'] = movies_links

df.sort_values("Year")

question_1 = df.copy().drop("Links", axis=1)

with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    print(question_1)


###### Question 2
#Get all actors from all movies:

# for movie_link in df["Links"]:
#     if movie_link != "":
#         page = urlopen(movie_link)
#         soup = BeautifulSoup(page, features="html.parser")
#         for elem in soup.find_all("h2", text=re.compile(r'[cast|Cast]')):
#             print (elem)
#         # nu = soup.findAll('h2', re.compile("(cast|Cast)"))
#         # print (nu)

# for movie_link in df["Links"]:
movie_link = df["Links"][5]
page = urlopen(movie_link)
soup = BeautifulSoup(page, features="html.parser")
for elem in soup.findAll("span", id=re.compile(r'[cast|Cast]$'), recursive=True):
    print (elem.get_text())
        # nu = soup.findAll('h2', re.compile("(cast|Cast)"))
        # print (nu)
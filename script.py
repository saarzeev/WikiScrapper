from urllib import urlopen
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

actors_list = []
link_list = []

for movie_link in df["Links"]:
    if movie_link == "":
        continue
    page = urlopen(movie_link)
    soup = BeautifulSoup(page, features="html.parser")
    html = list(soup.children)[2]
    body = list(html.children)[3]

    span = soup.findAll("span", id="Cast")
    if not span:
        span = soup.findAll("span", id="Principal cast")
    if not span:
        span = soup.findAll("span", id="Main cast")
    if not span:
        span = soup.findAll("span", id="Voice cast")
    if not span:
        # print("failed: " + movie_link)
        continue

    try:
        p = span[0].parent
        entire_list = list(p.findNext('ul').findAll("li"))
        for entry in entire_list:
            if entry.find('a'):
                name = entry.find('a').get_text()
                if not name=="Julia Roberts":
                    actors_list.append(name)
                    link_list.append(wiki_prefix + entry.find('a').get('href'))

            elif entry.get_text() != "":
                name = entry.get_text()
                if name.find(' as ') > -1:
                    name = name[:name.find(' as ')]
                if not name == "Julia Roberts":
                    actors_list.append(name)
                    link_list.append("")
    except:
        None


actorsdf=pd.DataFrame(actors_list, columns=['Name'])
actorsdf['Link'] = link_list
duplicated=actorsdf.groupby('Name').size().reset_index(name='Num of occurrences')
actorsdf.drop_duplicates(['Name'], keep="last",inplace=True)
actorsdf.sort_values("Name")

BD=[]
BP=[]
AW=[]

# count=0
# for co_actor_link in actorsdf["Link"]:
#     count=count+1
#     if co_actor_link == "":
#         BD.append("")
#         BP.append("")
#         continue
#     coactorpage = urlopen(co_actor_link)
#     soup = BeautifulSoup(coactorpage, features="html.parser")
#
#     try:
#         findTable = soup.find('table', class_='infobox biography vcard')
#         if not findTable:
#             BD.append("")
#             BP.append("")
#             continue
#         born=findTable.find('span',class_='bday')
#         if born:
#             bdate=(born.string).split("-")
#             BD.append(bdate[0])
#         else:
#             BD.append("")
#         birthplacesoup=findTable.find('div',class_='birthplace')
#         if birthplacesoup:
#             birthplace=(birthplacesoup.get_text()).split(",")
#             BP.append(birthplace[len(birthplace)-1])
#         else:
#             BP.append("")
#     except:
#         None

for co_actor_name in actorsdf["Name"]:
    try:
        # # names=co_actor_link.split('/')
        # # print names[len(names)-1]
        # # actorname=names[len(names)-1].replace()
        # # awardPage = urlopen("https://en.wikipedia.org/wiki/Category:Lists_of_awards_by_"+names[len(names)-1])
        # #  print count
        # s = actorsdf['Name']
        # name = s[count]
        # print name
        name = co_actor_name.replace(" ", "_")
        print name
        print
        # awardPage = urlopen("https://en.wikipedia.org/wiki/Category:Lists_of_awards_by_" + name)
        ur = "https://en.wikipedia.org/wiki/List_of_awards_and_nominations_received_by_" + name
        print ur
        awardPage = urlopen("https://en.wikipedia.org/wiki/List_of_awards_and_nominations_received_by_" + name)
        awardSoup = BeautifulSoup(awardPage, features="html.parser")
        i = 0;
        findAwards = awardSoup.findAll('table')
        if not findAwards:
            AW.append("A")
            print "A"
        else:
            # for tablefindAwards in findAwards:
            #     i =i + tablefindAwards.count("Won")
            i = str(findAwards).count("Won")
            AW.append(i)
            print i

    except:
        AW.append("B")
        print "b"

print len(AW)



# actorsdf['Birth year']=BD
# actorsdf['Birth palce']=BP
# actorsdf['Awards']=AW


print actorsdf


with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    print(actorsdf)


#TODO try and generalize line 80-85


###### Question 3
import matplotlib.pyplot as plt

print (duplicated)
dfHistogram=duplicated.groupby('Num of occurrences').size().reset_index(name ='count')
dfHistogram.plot(x='Num of occurrences',y='count',kind='bar')
plt.show()



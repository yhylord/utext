import csv
import re

import requests
import bs4 as BeautifulSoup
Soup = BeautifulSoup.BeautifulSoup

csv_file = open("Links.csv")
csv_list = csv.reader(csv_file)

csvdata1 = [row for row in csv_list]
x = 0

links = []
names =[]
#easier to just do 26th and 44th link seperate
for row in csvdata1:
    x = x+1
    #print (row[1] + str(x))
    #indexed x!= links aren't working with bs4 for some reason
    if x!=26 and x!=44 and x!=1 and x!=9 and x!=10 and x!=34 and x!=43 and x!=60:
        links.append(row[1])
        names.append(row[0])

#left out links:


links.append("https://cmhc.utexas.edu/thrive/")
names.append("CMHC - Thrive App")
links.append("http://deanofstudents.utexas.edu/emergency/titleix.php44")
names.append('Title IX - Report Incident')
links.append("https://texassports.com/")# ORIGINAL LINK DOES NOT CONTAIN WWW for some reason
names.append('Texas Athletics')
links.append("https://titleix.utexas.edu")
names.append('Title IX - Report Incident (1)')

print(names)
#these links have trouble with the parser
#links2.append(utexas parking links??)
#links2.append("http://www.utsenate.org")
#no registrar link provided
# no care couns link provided

def scrapSite(site):
    print(site + " is being indexed")
    r = requests.get(site)
    data = r.text

    soup = Soup(data,'html.parser')

    for script in soup(["script", "style"]):
        script.extract()    # rip it out

    # get text
    text = soup.get_text()
    text = text.replace(' ', '\n')
    text = text.replace('\n', ' ').replace('\r', '')

    text = re.sub(' +', ' ', text)
    text = re.sub(r'[^\w]', '', text)
    return text.encode('ascii', 'ignore').decode('ascii')



for website, name in zip(links, names):
    codedText = scrapSite(website)
    fileName = name + '.txt'
    with open('TextData/' + fileName, 'w') as f:
        f.write(codedText)





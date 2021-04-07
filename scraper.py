import requests
from bs4 import BeautifulSoup
from pandas import DataFrame

url = 'https://summerofcode.withgoogle.com/archive/2020/organizations/'
r = requests.get(url)
soup = BeautifulSoup(r.content, 'html.parser')
rows = soup.select('section div ul li')

link_list = []

for row in rows:
    abc = 'https://summerofcode.withgoogle.com' + row.select_one('a')['href']
    link_list.append(abc)

orgNames = []
contactLinks = []
techStack = []
slots = []
ideas = []

for org_url in link_list:
    lisat = []
    r = requests.get(org_url)
    soup = BeautifulSoup(r.text, 'html.parser')

    org = soup.find('div', class_="banner__text")
    orgNames.append(f"{org.h3.text}")

    technologies = soup.find_all('li', class_="organization__tag--technology")
    for technology in technologies:
        lisat.append(technology.text)

    mys = ', '.join(lisat)
    techStack.append(mys)

    irc = soup.select_one(".org__meta-button")['href']
    contactLinks.append(irc)

    projects = soup.find('ul', class_="project-list-container")
    slot = projects.findChildren('li')
    slots.append(len(slot))

    idea = soup.select_one(".org__button-container md-button")['href']
    ideas.append(idea)


table = {'Organizations': orgNames, 'Technologies': techStack,
         'Slots': slots, 'Ideas Page': ideas, 'Contact': contactLinks}

df = DataFrame(table)
export_csv = df.to_csv(r'gsoc-organizations-2020.csv')

print(r'Success!')

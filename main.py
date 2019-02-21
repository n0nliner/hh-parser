import requests
from bs4 import BeautifulSoup as bs
import pickle

logfile = 'web_works.txt'
n_pages = 14
page_url = 'https://spb.hh.ru/search/vacancy?clusters=true&enable_snippets=true&schedule=remote&specialization=1&text=web+developer'
headers = {'accept':'*/*','user-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}
skills = {}

for i in range(n_pages-1):
    session = requests.Session()
    response = session.get(page_url+f"&page={i}", headers=headers)
    if response.status_code == 200:
        print('OK')
        soup = bs(response.text, 'html.parser')
        links = soup.find_all('a', attrs={'class':'bloko-link'})
        urls = [ link["href"] for link in links ]
        for url in urls:
            try:
                session_url = requests.Session()
                response_unit = session_url.get(url, headers=headers)
                soup_unit = bs(response_unit.text, 'html.parser')
                skills_unit = [skll['title'] for skll in soup_unit.find_all('span', attrs={"class":"bloko-tag__section_text"})]
                for skillu in skills_unit:
                    try:
                        value = skills[skillu] + 1
                        skills.update({skillu:value})
                    except KeyError:
                        skills.update({skillu:1})
            except requests.exceptions.MissingSchema:#Exception as ex:
                continue
    else:
        print("error")


result = sorted(skills.items(), key=lambda kv: kv[1])
with open(logfile,'w+') as f:
    for el in result:
        f.write(f"{el[0]} : {el[1]}\n")

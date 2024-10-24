import requests
import json
from bs4 import BeautifulSoup

base_url = "https://search.envri.eu/notebookSearch/genericsearch?term=research&page="

def scrape_envri():
    page = 1
    github_links = []

    while True:
        response = requests.get(base_url + str(page))
        if response.status_code != 200:
            print(f"Stopping: No more pages found after page {page}")
            break
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        new_links = []
        for link in soup.find_all('a', href=True):
            href = link['href']
            if "github.com" in href:
                new_links.append(href)
        
        github_links.extend(new_links)
        print(f"Extract page #{page}, total number of new repositories: {len(new_links)}")

        page += 1

    return github_links

def write_repos_envri():

    repos_links = []
    software_links = scrape_envri()

    print(f"Total number of GitHub repositories scraped: {len(software_links)}")
    for link in software_links:
        repos_links.append({'community': 'ENVRI', 'githublink': link})

    with open('github_links_envri.json', 'w') as output_file:
        json.dump(repos_links, output_file, indent=4)

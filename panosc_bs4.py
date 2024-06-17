import requests
import json
import requests
from bs4 import BeautifulSoup

base_url = "https://software.pan-data.eu/software?page="
profile_url = "https://software.pan-data.eu"

def scrape_software_catalogue(page):

    response = requests.get(base_url + str(page))
    soup = BeautifulSoup(response.content, 'html.parser')
    links = []
    
    for a in soup.find_all('a', href=True):
        if a['href'].startswith('/software/'):
            links.append(profile_url + a['href'])
    return links

def extract_repos_panosc(profile_url):

    response = requests.get(profile_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    website_section = soup.find('td', text='Website')

    if website_section:
        link = website_section.find_next_sibling('td').find('a', href=True)
        if link and ('github.com' in link['href'] or 'gitlab.com' in link['href']):
            return link['href']
    
    return None 

def write_repos_panosc():

    repos_links = []
    for page in range(1, 10):
        print(f"Extracting for page {page}...")
        software_links = scrape_software_catalogue(page)
        for link in software_links:
            github_gitlab_link = extract_repos_panosc(link)
            if github_gitlab_link:
                repos_links.append(github_gitlab_link)

    with open(f'github_links_panosc.txt', 'w') as output_file:
        for link in repos_links:
            output_file.write(link + '\n')

    print(f"Extracted {len(repos_links)} GitHub & Gitlab links and saved to repo_links_panosc.txt")
    for link in repos_links:
        print(link)

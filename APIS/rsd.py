import requests
import json
from bs4 import BeautifulSoup

base_url = "https://research-software-directory.org"
search_url = "https://research-software-directory.org/software?order=mention_cnt&page="

def scrape_rsd():
    page = 1
    software_links = []
    previous_links_count = 0

    while True:

        response = requests.get(search_url + str(page) + "&rows=12")
        
        if response.status_code != 200:
            print(f"Stopping: No more pages found after page {page}")
            break
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        for link in soup.find_all('a', {'data-testid': 'software-masonry-card'}, href=True):
            href = link['href']
            full_link = base_url + href
            software_links.append(full_link)
        
        if len(software_links) == previous_links_count:
            print(f"No new links found on page #{page}. Stopping.")
            break
        
        previous_links_count = len(software_links)  
        print(f"Extracted links from page #{page}, total links so far: {len(software_links)}")
        page += 1

    return software_links

def extract_github_repo():

    github_links = []
    software_links = scrape_rsd()
    count = 1

    for link in software_links:
        try:
            response = requests.get(link)
            if response.status_code != 200:
                print(f"Failed to retrieve {link}")
                continue
            
            soup = BeautifulSoup(response.content, 'html.parser')

            github_link = soup.find('a', href=True, title= {"Github repository", "Repository", "Gitlab repository"})

            if github_link:

                github_href = github_link['href']
                github_links.append(github_href)
                print(f"Extracted repository link number#{count}")
                count +=1

            else:
                print(f"No repositpry link found on {link}")

        except Exception as e:
                    print(f"Error processing {link}: {e}")
                    continue
    
    return github_links

def write_repos_rsd():
    repos_links = []
    software_links = extract_github_repo()

    print(f"Total number of repositories scraped: {len(software_links)}")
    for link in software_links:
        repos_links.append({'community': 'RSD', 'repolink': link})

    with open('github_links_rsd.json', 'w') as output_file:
        json.dump(repos_links, output_file, indent=4)
import requests
import json
import time

def extract_data_ls_ri():
    page =1
    all_tools = []
    start_time = time.time()

    while True:
        response = requests.get("https://bio.tools/api/tool", 
                                params={'format': 'json',
                                        'page':page})
        
        if response.status_code == 200:
            data = response.json()
            all_tools.extend(data['list'])
            print(f"Extracting for page {page}...")
            if data['next']:
                page+= 1
            else:
                break
        
        else:
            print("Failed to retrieve data:", response.status_code)

    with open(f'response_ls_ri.json', 'w') as json_file:
        json.dump(all_tools, json_file, indent=4)
    
    end_time = time.time()  
    total_time = end_time - start_time
    
    print(f"Successfully retrieved and saved all data in {total_time:.2f} seconds")


def extract_repos_ls_ri():
    github_links = []
    with open(f'response_ls_ri.json', 'r') as file:
        data = json.load(file)
        print("Opened & loaded successfully")

    # In LS-RI case, after analyzing the data retieved by the API, I concluded that the GitHub links are mentioned in the "homepage" section
    for entry in data:
        if 'homepage' in entry and ('github.com' or 'gitlab.com'in entry['homepage']):
            name = entry['name']
            github_url = entry['homepage']
            github_links.append({"name": name, "github_url": github_url})

        with open("github_links_ls_ri.txt", "w") as output_file:
            for entry in github_links:
                github_url = entry["github_url"]
                output_file.write(github_url + "\n")

    print(f"Extracted {len(github_links)} GitHub links and saved to github_links_ls_ri.txt")
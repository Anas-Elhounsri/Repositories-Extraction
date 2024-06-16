import requests
import json
import time

type = 'software'
page = 1
all_tools_xml_str = ""
all_tools = []

# community_1 = 'sshoc'
# community_2 = 'escape2020'
# community_3 = 'LS-RI'
# community_4 = 'PANOSC'

def zenodo_api(community, token):
# For using Zenodo, you need to have an access token, you can get the token for their website
    response = requests.get("https://zenodo.org/api/records",
                            params={
                                'communities': community,
                                'type': type,
                                'access_token': token})

    if response.status_code == 200:
        with open(f'response_{community}.json', 'w') as json_file:
            json.dump(response.json(), json_file, indent=4)
            print("Successfully retrieved data")
    else:
        print("Failed to retrieve data:", response.status_code)

def bio_tools_api():
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


def extract_repos_zenodo(community):
    github_links = []
    with open(f'response_{community}.json', 'r') as file:
        data = json.load(file)
        print("Opened & loaded successfully")

    # Here we are accessing "related_identifiers" section of the json file that contains the github links if available
    for entry in data['hits']['hits']:
        if 'related_identifiers' in entry['metadata']:
            for identifier in entry['metadata']['related_identifiers']:
                if identifier['scheme'] == 'url' and 'github.com' in identifier['identifier']:
                    github_links.append(identifier['identifier'])

    # After extracting the links and adding them to a list, we create a txt file for the respective cluster
    with open(f'github_links_{community}.txt', 'w') as output_file:
        for link in github_links:
            output_file.write(link + '\n')

    print(f"Extracted {len(github_links)} GitHub links and saved to github_links_{community}.txt")

def extract_repos_ls_ri():
    github_links = []
    with open(f'response_ls_ri.json', 'r') as file:
        data = json.load(file)
        print("Opened & loaded successfully")

    # In LS-RI case, after analyzing the data retieved by the API, I concluded that the GitHub links are mentioned in the "homepage" section
    for entry in data:
        if 'homepage' in entry and 'github.com' in entry['homepage']:
            name = entry['name']
            github_url = entry['homepage']
            github_links.append({"name": name, "github_url": github_url})

        with open("github_links_ls_ri.txt", "w") as output_file:
            for entry in github_links:
                github_url = entry["github_url"]
                output_file.write(github_url + "\n")

    print(f"Extracted {len(github_links)} GitHub links and saved to github_links_ls_ri.txt")


if __name__ == "__main__":

    community =""
    while community != 's':
        print("")
        community = input("Choose the community you wish to extract data from (type 's' to stop):\n\n- sshoc\n- escape2020\n- LS-RI \n- PANOSC (In progess)\n\nInput:").lower()
        
        if community != 's' and community == 'sshoc' or community == 'escape2020':
            ACCESS_TOKEN = input("Please input your access token: ")
            print("")
            print("----------------------------------------------")
            zenodo_api(community, token = ACCESS_TOKEN)
            extract_repos_zenodo(community)
            print("----------------------------------------------")
            print("")

        elif community != 's' and community == 'ls-ri':
            print("")
            print("----------------------------------------------")
            bio_tools_api()
            extract_repos_ls_ri()
            print("----------------------------------------------")

    print("")
    print("Exited successfully.")
    print("")
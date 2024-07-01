import requests
import json

type = 'software'

def extract_data_zenodo(community, token):
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

def extract_repos_zenodo(community):
    github_links = []
    with open(f'response_{community}.json', 'r') as file:
        data = json.load(file)
        print("Opened & loaded successfully")

    # Here we are accessing "related_identifiers" section of the json file that contains the github links if available
    for entry in data['hits']['hits']:
        if 'related_identifiers' in entry['metadata']:
            for identifier in entry['metadata']['related_identifiers']:
                if identifier['scheme'] == 'url' and ('github.com' in identifier['identifier'] or 'gitlab.com' in identifier['identifier']):
                    github_links.append({'community': community, 'githublink': identifier['identifier']})

    # After extracting the links and adding them to a list, we create a txt file for the respective cluster
    with open(f'github_links_{community}.json', 'w') as output_file:
        json.dump(github_links, output_file, indent=4)

    print(f"Extracted {len(github_links)} GitHub links and saved to github_links_{community}.json")

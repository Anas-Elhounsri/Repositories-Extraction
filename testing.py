import requests
import json
import xml.dom.minidom
import time


ACCESS_TOKEN = ''

type = 'software'
page = 1
all_tools_xml_str = ""
all_tools = []

# community_1 = 'sshoc'
# community_2 = 'escape2020'
# community_3 = 'LS-RI'
# community_4 = 'PANOSC'

def zenodo_api(community):
# For using Zenodo, you need to have an access token, you can get the token for their website
    response = requests.get("https://zenodo.org/api/records",
                            params={
                                'communities': community,
                                'type': type,
                                'access_token': ACCESS_TOKEN})

    if response.status_code == 200:
        with open(f'response_{community}.json', 'w') as json_file:
            json.dump(response.json(), json_file, indent=4)
            print("Successfully retrieved data")
    else:
        print("Failed to retrieve data:", response.status_code)

def bio_tools_api(page):
    response = requests.get("https://bio.tools/api/tool", 
                            params={'format': 'xml',
                                    'page':page})
    
    if response.status_code == 200:
        return response.text

        # with open(f'response_ls_ri.xml', 'w') as xml_file:
        #     xml_file.write(pretty_xml_str)
        #     print("Successfully retrieved data")
        #     return response.text
        
    else:
        print("Failed to retrieve data:", response.status_code)
        


def extract_repos_json(community):

    with open(f'response_{community}.json', 'r') as file:
        data_sshoc = json.load(file)
        print("Opened & loaded successfully")

    github_links = []

    # Here we are accessing "related_identifiers" section of the json file that contains the github links if available
    for entry in data_sshoc['hits']['hits']:
        if 'related_identifiers' in entry['metadata']:
            for identifier in entry['metadata']['related_identifiers']:
                if identifier['scheme'] == 'url' and 'github.com' in identifier['identifier']:
                    github_links.append(identifier['identifier'])

    # After extracting the links and adding them to a list, we create a txt file for the respective cluster
    with open(f'github_links_{community}.txt', 'w') as output_file:
        for link in github_links:
            output_file.write(link + '\n')

    print(f"Extracted {len(github_links)} GitHub links and saved to github_links_{community}.txt")

# def extract_repos_xml(community):

community =""
while community != 's':
    
    community = input("Choose the community you wish to extract data from (type 's' to stop):\n- sshoc\n- escape2020\n- LS-RI (In progress not yet finished)\nInput:").lower()

    if community != 's' and community == 'sshoc' or community == 'escape2020':
        print("")
        print("----------------------------------------------")
        zenodo_api(community)
        extract_repos_json(community)
        print("----------------------------------------------")
        print("")

    elif community != 's' and community == 'ls-ri':
        print("")
        
        start_time = time.time()
        while True:
            
            print(f"Fetching page {page}...")
            tools_xml_str = bio_tools_api(page)
            if tools_xml_str:

                # We will be parsing the current page's XML
                xml_dom = xml.dom.minidom.parseString(tools_xml_str)
                tools = xml_dom.getElementsByTagName("tool")
                all_tools.extend(tools)
                page += 1

            else:
                break

        # We need to combine all the tools under a single root element
        combined_xml_str = '<tools>'
        for tool in all_tools:
            combined_xml_str += tool.toxml()
        combined_xml_str += '</tools>'

        combined_xml_dom = xml.dom.minidom.parseString(combined_xml_str)
        pretty_combined_xml_str = combined_xml_dom.toprettyxml(indent="  ")

        with open("tools_sequence_alignment_pretty.xml", "w") as file:
            file.write(pretty_combined_xml_str)

        print("Data saved to response_ls_ri.xml")
        print("")

        end_time = time.time()
        execution_time = end_time - start_time

        print(f"Script execution time: {execution_time:.2f} seconds")

    else:
        continue

print("")
print("Exited successfully .")
> [!WARNING]
> This is still in progress and subject to change, as additional requirements may arise.

# Repositories Extraction:
- ESCAPE OSSR (Available)
- SSHOC (Available)
- LI-RS (Available)
- PANOSC (Available)
- ENVRI (In progress)

## How to run:
- Install the required libraries with `requirements.txt`:
``` bash
pip install -r requirements.txt
```
- Run the script by running `main.py` file, then choose the community from the list that you wish you extract data from : *(Note for `SSHOC` and `ESCAPE` communities, you need to get an access token from [Zenodo](https://zenodo.org/account/settings/applications/tokens/new/))*

``` bash
Choose the community you wish to extract data from (type 's' to stop):

- sshoc
- escape2020
- LS-RI 
- PANOSC

Input:
```
- Example output:
``` bash
Input:sshoc
Please input your access token: <Your access token>

----------------------------------------------
Successfully retrieved data
Opened & loaded successfully
Extracted 6 GitHub links and saved to github_links_sshoc.txt
----------------------------------------------
```
- On you local directory you will see the datasets extracted, both the `JSON` and the `txt` file of GitHub links for *SSHOC, ESCAPE OSSR* and *LS-RI*, as for *PANOSC*, we extract the links directly with `bs4` library.

## The Process:
### For SSHOC & ESCAPE OSSR:
Zenodo is offers an API service that allows us to extract the necessary information needed for our case, by accessing their repository through the endpoint https://zenodo.org/api/records :
 ``` python 
response = requests.get("https://zenodo.org/api/records",
                            params={
                                'communities': community,
                                'type': type,
                                'access_token': token})
 ```
Where in `community`, we specify whether we want *SSHOC* or *ESCAPE OSSR*, In `type ` we spcify to only list software since the rest of the tags are publications, presentations videos etc... that are outside the scope of our project. Finally we have  `access_token`, where you can get it from [Zenodo](https://zenodo.org/account/settings/applications/tokens/new/) after creating an account.

This will extract all available tools for either SSHOC or ESCAPE OSSR as a JSON file, then it will access the file to extract only the GitHub or GitLab repository from the "Identifier" section.

This will store two JSON files, one has the original metadata, and the other as GitHub and GitLab links.

### For LS-RI (bio.tools):
Similarly, bio.tools offers an API to extract all the tools available on their repository, this time, all the data in LS-RI are tools, some have the GitHub or GitLab link, we use  `format` to extract it as JSON file, the links are usually stored in the hompage section of the JSON file.

This script extracts approximately 15,000 links, and stores it separately as two JSON files

### For PANOSC:
For this cluster, since they did not offer an API, I extracted data with webscraping using `bs4` library, and it extracts 23 links. and directly stores them as JSON.

# Repositories Extraction:
- ESCAPE OSSR (Available)
- SSHOC (Available)
- LI-RS (Available)
- PANOSC (Not available yet)

# How to run:
- Install the required libraries with `requirements.txt`:
``` bash
pip install -r requirements.txt
```
- Run the script then choose the community from the list that you wish you extract data from : *(Note for `SSHOC` and `ESCAPE` communities, you need to get an access token from [Zenodo](https://zenodo.org/account/settings/applications/tokens/new/))*

``` bash
Choose the community you wish to extract data from (type 's' to stop):

- sshoc
- escape2020
- LS-RI 
- PANOSC (In progess)

Input:
```
- Example output:
``` bash
Input:sshoc
Please input your access token: Qeh4v706RtGlnbiXN4PQ3Vyxs9YR1wxZTLOcp5wGiowq1hbAiBZuUsi9wiXm


----------------------------------------------
Successfully retrieved data
Opened & loaded successfully
Extracted 6 GitHub links and saved to github_links_sshoc.txt
----------------------------------------------
```
- On you local directory you will see the datasets extracted, both the `JSON` and the `txt` file of GitHub links. 

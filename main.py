from zenodo_api import extract_data_zenodo, extract_repos_zenodo
from ls_ri_api import extract_data_ls_ri, extract_repos_ls_ri
from panosc_bs4 import write_repos_panosc

def main():

    community =""
    while community != 's':
        print("")
        community = input("Choose the community you wish to extract data from (type 's' to stop):\n\n- sshoc\n- escape2020\n- LS-RI \n- PANOSC\n\nInput:").lower()
        
        if community != 's' and community == 'sshoc' or community == 'escape2020':
            ACCESS_TOKEN = input("Please input your access token: ")
            print("")
            print("----------------------------------------------")
            extract_data_zenodo(community, token = ACCESS_TOKEN)
            extract_repos_zenodo(community)
            print("----------------------------------------------")
            print("")

        elif community != 's' and community == 'ls-ri':
            print("")
            print("----------------------------------------------")
            extract_data_ls_ri()
            extract_repos_ls_ri()
            print("----------------------------------------------")
        
        elif community != 's' and community == 'panosc':
            print("")
            print("----------------------------------------------")
            write_repos_panosc()
            print("----------------------------------------------")


    print("")
    print("Exited successfully.")
    print("")

if __name__ == "__main__":
    main()
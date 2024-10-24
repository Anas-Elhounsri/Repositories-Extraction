import sys

module_path= '\\APIS'

if module_path not in sys.path:
    sys.path.insert(0, f'{sys.path[0]}{module_path}')


from zenodo_api import extract_data_zenodo, extract_repos_zenodo
from ls_ri_api import extract_data_ls_ri, extract_repos_ls_ri
from panosc_bs4 import write_repos_panosc
from envri import write_repos_envri
from rsd import write_repos_rsd

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

        elif community != 's' and community == 'envri':
            print("")
            print("----------------------------------------------")
            write_repos_envri()
            print("----------------------------------------------")

        elif community != 's' and community == 'rsd':
            print("")
            print("----------------------------------------------")
            write_repos_rsd()
            print("----------------------------------------------")



    print("")
    print("Exited successfully.")
    print("")

if __name__ == "__main__":
    main()